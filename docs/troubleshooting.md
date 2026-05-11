# Troubleshooting

## Wazuh Agent Does Not Appear

- Confirm the Windows agent service is running:

```powershell
net start wazuhsvc
```

- Confirm the Wazuh manager address in the agent install command is correct.
- Check cloud firewall rules and local Windows firewall behavior.
- Restart the Windows agent after changes to `ossec.conf`.

## Sysmon Events Do Not Reach Wazuh

- Confirm Sysmon is installed.
- Check Event Viewer under `Applications and Services Logs > Microsoft > Windows > Sysmon`.
- Confirm the Wazuh agent `ossec.conf` includes the Sysmon event channel.
- Restart the Wazuh agent service after editing configuration.

## Mimikatz Events Are Missing From Wazuh Discover

- Confirm Wazuh archives are enabled in `/var/ossec/etc/ossec.conf`:

```xml
<logall>yes</logall>
<logall_json>yes</logall_json>
```

- Restart Wazuh manager:

```bash
systemctl restart wazuh-manager.service
```

- Confirm Filebeat is reading archives.
- Search the archive log directly:

```bash
cat /var/ossec/logs/archives/archives.log | grep -i mimikatz
```

## Custom Rule Does Not Trigger

- Confirm the rule is saved in `local_rules.xml`.
- Confirm the rule ID is unique, for example `100002`.
- Confirm the field name uses Wazuh's extracted Sysmon field:

```xml
win.eventdata.originalFileName
```

- Restart Wazuh manager after saving the rule.
- Rename the executable and retest to confirm `originalFileName` is doing the detection work.

## Shuffle Does Not Receive Alerts

- Confirm the Wazuh integration points to your real Shuffle webhook URL.
- Replace broad level-based forwarding with the specific rule ID when testing this lab:

```xml
<rule_id>100002</rule_id>
```

- Restart Wazuh manager.
- Start or rerun the Shuffle workflow and inspect execution details.

## VirusTotal Query Fails

- Confirm the Shuffle regex extracts only the SHA256 value, not the entire `SHA256=<hash>` string.
- Use this capture group:

```regex
SHA256=([0-9A-Fa-f]{64})
```

- Confirm the VirusTotal app is authenticated.
- A successful API connection should return HTTP `200`.

## TheHive Alert Does Not Appear

- Confirm TheHive is reachable on port `9000`.
- Confirm Cassandra, Elasticsearch, and TheHive services are all running:

```bash
systemctl status cassandra.service
systemctl status elasticsearch
systemctl status thehive
```

- Confirm the Shuffle TheHive app uses the correct URL and API key.
- Confirm the cloud firewall allows Shuffle to reach TheHive.

## Email Notification Does Not Arrive

- Confirm the email node is connected after VirusTotal or the final enrichment step.
- Check the configured recipient, subject, and body.
- Inspect the Shuffle execution output for mail-provider or authentication errors.
