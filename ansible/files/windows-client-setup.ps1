# Secure Windows client setup for AWS VM SSH access

# === CONFIGURE THESE ===
$AWS_VM_IP = "YOUR_AWS_VM_PUBLIC_IP"
$SSH_USER = "Administrator"  # or your Windows user
$AWS_PUB_KEY = "ssh-rsa AAAAB3Nza... your-aws-public-key ... user@aws-vm"

$sshDir = "C:\Users\$SSH_USER\.ssh"
$authKeysFile = "$sshDir\authorized_keys"

# Ensure .ssh directory exists
if (-not (Test-Path -Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force
}

# Add AWS public key if not already present
if (-not (Select-String -Path $authKeysFile -Pattern [regex]::Escape($AWS_PUB_KEY) -Quiet)) {
    Add-Content -Path $authKeysFile -Value $AWS_PUB_KEY
}

# Set permissions (simplified)
icacls $sshDir /inheritance:r
icacls $sshDir /grant "$SSH_USER:(R,W)"
icacls $authKeysFile /inheritance:r
icacls $authKeysFile /grant "$SSH_USER:(R,W)"

# Enable and start sshd service (assumes OpenSSH installed)
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Disable password authentication in sshd_config
$sshdConfigPath = "$env:ProgramData\ssh\sshd_config"
$config = Get-Content $sshdConfigPath
if ($config -match 'PasswordAuthentication yes') {
    $config = $config -replace 'PasswordAuthentication yes', 'PasswordAuthentication no'
    $config | Set-Content $sshdConfigPath
} elseif (-not ($config -match 'PasswordAuthentication no')) {
    Add-Content $sshdConfigPath "PasswordAuthentication no"
}

Restart-Service sshd

# Setup Windows Firewall to allow SSH only from AWS VM IP
New-NetFirewallRule -DisplayName "Allow SSH from AWS VM" -Direction Inbound -LocalPort 22 -Protocol TCP -RemoteAddress $AWS_VM_IP -Action Allow

# Block other SSH connections
New-NetFirewallRule -DisplayName "Block SSH from other IPs" -Direction Inbound -LocalPort 22 -Protocol TCP -RemoteAddress Any -Action Block -Priority 4096

Write-Host "Windows client setup complete. SSH locked to AWS VM IP: $AWS_VM_IP"
