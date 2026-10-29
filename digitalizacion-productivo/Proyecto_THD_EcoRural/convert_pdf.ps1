$docxPath = "C:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\digitalizacion-productivo\Proyecto_THD_EcoRural\Plan_Digitalizacion_THD_EcoRural_Kevin.docx"
$pdfPath  = "C:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\digitalizacion-productivo\Proyecto_THD_EcoRural\Plan_Digitalizacion_THD_EcoRural_Kevin.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Host "PDF export successful: $pdfPath"
} catch {
    Write-Host "Error during PDF export: $_"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
