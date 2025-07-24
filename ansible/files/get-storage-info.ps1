# Sample Input: No arguments needed; run on the VM itself

$outputFileTxt = "storage_info_{0}.txt" -f (Get-Date -Format 'yyyy-MM-dd')

$diskInfoText = Get-WmiObject Win32_LogicalDisk | ForEach-Object {
    $sizeGB = "{0:N2}" -f ($_.Size / 1GB)
    $freeGB = "{0:N2}" -f ($_.FreeSpace / 1GB)
    $usedGB = "{0:N2}" -f ( ($_.Size - $_.FreeSpace) / 1GB)
    $usagePercent = "{0:N2}" -f ( ( ($_.Size - $_.FreeSpace) / $_.Size) * 100 )
    
    "Drive $($_.DeviceID):"
    "  FileSystem : $($_.FileSystem)"
    "  Size (GB)  : $sizeGB"
    "  Used (GB)  : $usedGB"
    "  Free (GB)  : $freeGB"
    "  Usage (%)  : $usagePercent`%"
    ""
}

$diskInfoText | Out-File $outputFileTxt
Write-Host "Storage info saved to $outputFileTxt"

$outputFileCsv = "storage_info_$(Get-Date -Format 'yyyy-MM-dd').csv"

$diskInfoCsv = Get-WmiObject Win32_LogicalDisk | Select-Object DeviceID, FileSystem, 
    @{Name="SizeGB";Expression={[math]::Round($_.Size/1GB,2)}}, 
    @{Name="FreeGB";Expression={[math]::Round($_.FreeSpace/1GB,2)}}, 
    @{Name="UsedGB";Expression={[math]::Round( ($_.Size - $_.FreeSpace)/1GB,2)}}, 
    @{Name="UsagePercent";Expression={[math]::Round( ( ($_.Size - $_.FreeSpace)/$_.Size)*100,2)}}

$diskInfoCsv | Export-Csv -Path $outputFileCsv -NoTypeInformation
Write-Host "Storage CSV info saved to $outputFileCsv"