# Security Notes

This project is a defensive SOC automation lab. It includes security tooling and malware-adjacent telemetry generation, so keep the work inside a controlled environment.

## Approved Scope

- Use virtual machines, cloud droplets, or lab hosts that you own or are explicitly authorized to test.
- Use Mimikatz only as a controlled detection artifact for generating telemetry.
- Do not use real production credentials, customer data, or personal accounts inside the test endpoint.
- Keep Wazuh, TheHive, and Shuffle credentials unique to the lab.

## Network Exposure

- Restrict cloud firewall rules to your own source IP wherever possible.
- Expose TheHive port `9000` only when needed, and preferably only from trusted IP ranges.
- Expose Wazuh web access only to your own IP.
- Avoid leaving permissive inbound rules in place after testing.

## Secrets Handling

Do not commit:

- Shuffle webhook URLs.
- VirusTotal API keys.
- TheHive API keys.
- Generated Wazuh admin passwords.
- Public IP addresses tied to an active personal lab, if you do not want them disclosed.

Use placeholders in documentation and configuration examples:

```text
<WAZUH_PUBLIC_IP>
<THEHIVE_PUBLIC_IP>
<SHUFFLE_WEBHOOK_URL>
<VIRUSTOTAL_API_KEY>
<THEHIVE_API_KEY>
```

## Lab Cleanup

When the lab is complete:

1. Power off or destroy temporary cloud droplets.
2. Remove permissive firewall rules.
3. Revoke API keys used during testing.
4. Delete snapshots that contain secrets.
5. Re-enable Windows Defender settings changed for telemetry generation.
