"""
よく依頼されるVBAパターンのテンプレート集
Claude Codeと組み合わせて使う: テンプレを渡して案件仕様に合わせて改変してもらう
"""

TEMPLATES = {
    "csv_import": {
        "description": "CSVファイルを読み込んでシートに貼り付け",
        "code": '''
Sub ImportCSV()
    Dim filePath As String
    Dim ws As Worksheet
    Dim conn As Object
    Dim rs As Object

    filePath = Application.GetOpenFilename("CSVファイル,*.csv")
    If filePath = "False" Then Exit Sub

    Set ws = ThisWorkbook.Sheets(1)
    ws.Cells.Clear

    ' CSVをADOで読み込み（文字コード対応）
    Set conn = CreateObject("ADODB.Connection")
    conn.Open "Provider=Microsoft.Jet.OLEDB.4.0;" & _
              "Data Source=" & Left(filePath, InStrRev(filePath, "\")) & ";" & _
              "Extended Properties='text;HDR=YES;FMT=Delimited'"

    Set rs = CreateObject("ADODB.Recordset")
    rs.Open "SELECT * FROM [" & Mid(filePath, InStrRev(filePath, "\") + 1) & "]", conn

    ' ヘッダ出力
    Dim i As Integer
    For i = 0 To rs.Fields.Count - 1
        ws.Cells(1, i + 1).Value = rs.Fields(i).Name
    Next i

    ' データ出力
    ws.Range("A2").CopyFromRecordset rs

    rs.Close: conn.Close
    MsgBox "インポート完了"
End Sub
''',
    },
    "data_dedup": {
        "description": "指定列の重複行を削除",
        "code": '''
Sub RemoveDuplicates()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim keyCol As Integer

    Set ws = ActiveSheet
    keyCol = 1  ' 重複チェックする列番号（A列=1）
    lastRow = ws.Cells(ws.Rows.Count, keyCol).End(xlUp).Row

    ' 下から上に走査して重複削除
    Dim i As Long
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")

    For i = lastRow To 2 Step -1
        Dim key As String
        key = ws.Cells(i, keyCol).Value
        If dict.Exists(key) Then
            ws.Rows(i).Delete
        Else
            dict.Add key, True
        End If
    Next i

    MsgBox "重複削除完了。残り行数: " & ws.Cells(ws.Rows.Count, keyCol).End(xlUp).Row - 1
End Sub
''',
    },
    "auto_filter_export": {
        "description": "フィルタで絞り込んだデータを別シートへエクスポート",
        "code": '''
Sub FilterAndExport()
    Dim srcWs As Worksheet
    Dim dstWs As Worksheet
    Dim filterCol As Integer
    Dim filterVal As String

    Set srcWs = ThisWorkbook.Sheets("データ")
    filterCol = 3   ' フィルタする列番号
    filterVal = "対象"  ' フィルタ値

    ' 出力先シートを作成（既存なら削除）
    On Error Resume Next
    Application.DisplayAlerts = False
    ThisWorkbook.Sheets("エクスポート").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    Set dstWs = ThisWorkbook.Sheets.Add
    dstWs.Name = "エクスポート"

    ' フィルタ適用してコピー
    srcWs.UsedRange.AutoFilter Field:=filterCol, Criteria1:=filterVal
    srcWs.UsedRange.SpecialCells(xlCellTypeVisible).Copy dstWs.Range("A1")
    srcWs.AutoFilterMode = False

    MsgBox "エクスポート完了: " & dstWs.UsedRange.Rows.Count - 1 & " 件"
End Sub
''',
    },
    "mail_send": {
        "description": "Outlookで一括メール送信（Excelリストから）",
        "code": '''
Sub SendBulkMail()
    Dim ws As Worksheet
    Dim outApp As Object
    Dim outMail As Object
    Dim lastRow As Long
    Dim i As Long

    Set ws = ThisWorkbook.Sheets("送信リスト")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    Set outApp = CreateObject("Outlook.Application")

    For i = 2 To lastRow
        ' A列:宛先, B列:氏名, C列:件名, D列:本文
        If ws.Cells(i, 1).Value = "" Then GoTo Continue

        Set outMail = outApp.CreateItem(0)
        With outMail
            .To = ws.Cells(i, 1).Value
            .Subject = ws.Cells(i, 3).Value
            .Body = "Dear " & ws.Cells(i, 2).Value & "," & vbCrLf & vbCrLf & ws.Cells(i, 4).Value
            .Send  ' .Display に変えると確認画面が出る
        End With

        ws.Cells(i, 5).Value = "送信済"  ' E列にステータス記入
Continue:
    Next i

    MsgBox "送信完了"
End Sub
''',
    },
    "pdf_export": {
        "description": "指定シートをPDFとして保存",
        "code": '''
Sub ExportToPDF()
    Dim ws As Worksheet
    Dim savePath As String

    Set ws = ActiveSheet
    savePath = ThisWorkbook.Path & "\" & ws.Name & "_" & Format(Now, "YYYYMMDD") & ".pdf"

    ws.ExportAsFixedFormat _
        Type:=xlTypePDF, _
        Filename:=savePath, _
        Quality:=xlQualityStandard, _
        IncludeDocProperties:=True, _
        IgnorePrintAreas:=False

    MsgBox "PDF保存完了: " & savePath
End Sub
''',
    },
}


def list_templates():
    print("利用可能なVBAテンプレート:\n")
    for key, val in TEMPLATES.items():
        print(f"  [{key}]  {val['description']}")


def get_template(name: str) -> str:
    if name not in TEMPLATES:
        return f"テンプレート '{name}' は存在しません。list_templates() で確認してください。"
    return TEMPLATES[name]["code"].strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        list_templates()
    else:
        print(get_template(sys.argv[1]))
