# Security Orchestration, Automation, and Response Engineering Guide

This guide converts the original PDF lab into a GitHub-friendly implementation document. It keeps the same technical flow while making commands, configuration, screenshots, and decision points easier to follow.

## 1. Objective

**Visual walkthrough: Project overview**

Build a defensive SOC automation workflow that:

- Collects endpoint telemetry from a Windows 10 client.
- Uses Sysmon for detailed Windows event generation.
- Sends Windows telemetry into Wazuh.
- Detects Mimikatz-like activity with a custom Wazuh rule.
- Sends the alert to Shuffle through a webhook.
- Extracts a SHA256 hash and checks reputation with VirusTotal.
- Creates an alert in TheHive.
- Sends an email notification to a SOC analyst.

## 2. Prerequisites

### Hardware

- Host machine capable of running multiple virtual machines, or access to cloud infrastructure.
- Enough CPU, RAM, and disk capacity for:
  - Windows 10 client VM.
  - Wazuh server.
  - TheHive server.

### Software and Platforms

- VMware Workstation, VMware Fusion, or another hypervisor.
- Windows 10 client VM.
- Ubuntu 22.04 for Wazuh.
- Ubuntu 22.04 for TheHive.
- Sysmon.
- Sysmon Modular configuration.
- Wazuh.
- Shuffle.
- TheHive.
- VirusTotal account and API key.

> The source PDF specifically recommends Ubuntu 22.04 because later Ubuntu versions may introduce dependency problems with the selected stack.

### Skills Assumed

- Basic VM setup.
- Basic Linux command-line usage.
- Familiarity with Windows Event Viewer.
- Basic SOC concepts: telemetry, alerts, enrichment, case management, and response workflows.

## 3. Lab Architecture

```mermaid
sequenceDiagram
    participant Endpoint as Windows 10 + Sysmon
    participant Wazuh as Wazuh Manager
    participant Shuffle as Shuffle SOAR
    participant VT as VirusTotal
    participant Hive as TheHive
    participant Analyst as SOC Analyst

    Endpoint->>Wazuh: Sysmon event telemetry
    Wazuh->>Wazuh: Custom rule 100002 detects Mimikatz
    Wazuh->>Shuffle: Alert JSON through webhook
    Shuffle->>Shuffle: Extract SHA256 with regex
    Shuffle->>VT: Query hash reputation
    VT-->>Shuffle: Reputation result
    Shuffle->>Hive: Create alert
    Shuffle->>Analyst: Send email notification
```

## 4. Configure Windows 10 and Sysmon

**Visual walkthrough: Windows 10 and Sysmon setup**

![Windows 10 and Sysmon setup screenshot page 4 image 1](../assets/images/page-04-image-01.png)

![Windows 10 and Sysmon setup screenshot page 5 image 1](../assets/images/page-05-image-01.png)

![Windows 10 and Sysmon setup screenshot page 6 image 1](../assets/images/page-06-image-01.png)

![Windows 10 and Sysmon setup screenshot page 6 image 2](../assets/images/page-06-image-02.png)

![Windows 10 and Sysmon setup screenshot page 7 image 1](../assets/images/page-07-image-01.png)

![Windows 10 and Sysmon setup screenshot page 8 image 1](../assets/images/page-08-image-01.png)

![Windows 10 and Sysmon setup screenshot page 8 image 2](../assets/images/page-08-image-02.png)

![Windows 10 and Sysmon setup screenshot page 9 image 1](../assets/images/page-09-image-01.png)


### 4.1 Install Windows 10

Create a Windows 10 virtual machine in VMware or your preferred hypervisor. This endpoint is the telemetry source for the lab.

### 4.2 Download Sysmon

Download Sysmon from Microsoft Sysinternals.

### 4.3 Download Sysmon Configuration

Download a Sysmon Modular configuration and locate:

```text
sysmonconfig.xml
```

Place `sysmonconfig.xml` in the extracted Sysmon directory.

### 4.4 Install Sysmon

Open PowerShell as Administrator, move into the Sysmon directory, and run:

```powershell
.\Sysmon64.exe -i .\sysmonconfig.xml
```

Verify Sysmon through:

- Windows Services.
- Event Viewer.
- `Applications and Services Logs > Microsoft > Windows > Sysmon`.

## 5. Set Up Wazuh

**Visual walkthrough: Wazuh server deployment and access**

![Wazuh server deployment and access screenshot page 10 image 1](../assets/images/page-10-image-01.jpg)

![Wazuh server deployment and access screenshot page 10 image 2](../assets/images/page-10-image-02.png)

![Wazuh server deployment and access screenshot page 11 image 1](../assets/images/page-11-image-01.png)

![Wazuh server deployment and access screenshot page 11 image 2](../assets/images/page-11-image-02.png)

![Wazuh server deployment and access screenshot page 11 image 3](../assets/images/page-11-image-03.png)

![Wazuh server deployment and access screenshot page 12 image 1](../assets/images/page-12-image-01.png)

![Wazuh server deployment and access screenshot page 12 image 2](../assets/images/page-12-image-02.png)

![Wazuh server deployment and access screenshot page 13 image 1](../assets/images/page-13-image-01.png)

![Wazuh server deployment and access screenshot page 14 image 1](../assets/images/page-14-image-01.png)

![Wazuh server deployment and access screenshot page 15 image 1](../assets/images/page-15-image-01.png)

![Wazuh server deployment and access screenshot page 16 image 1](../assets/images/page-16-image-01.png)

![Wazuh server deployment and access screenshot page 16 image 2](../assets/images/page-16-image-02.png)


### 5.1 Create the Wazuh Server

Create an Ubuntu 22.04 server. The original lab uses a DigitalOcean Droplet named `Wazuh`, but another cloud provider or VM is acceptable.

### 5.2 Restrict Firewall Access

Create firewall rules that allow access only from your own IP address where possible.

Typical access needs:

- Wazuh dashboard over HTTPS.
- SSH from your IP.
- Wazuh agent communication ports according to your Wazuh deployment.

### 5.3 Update the Server

Connect to the Wazuh server and update packages:

```bash
sudo apt-get update && sudo apt-get upgrade
```

### 5.4 Install Wazuh

Run the Wazuh all-in-one installation script:

```bash
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

Record the generated `admin` password.

```text
User: admin
Password: <GENERATED_PASSWORD>
```

### 5.5 Access the Wazuh Web Interface

Open:

```text
https://<WAZUH_PUBLIC_IP>
```

Because this lab uses a self-signed certificate, your browser may warn you. Proceed only if this is your controlled lab server.

## 6. Install TheHive

**Visual walkthrough: TheHive server installation**

![TheHive server installation screenshot page 17 image 1](../assets/images/page-17-image-01.png)

![TheHive server installation screenshot page 18 image 1](../assets/images/page-18-image-01.png)

![TheHive server installation screenshot page 20 image 1](../assets/images/page-20-image-01.png)


### 6.1 Create the TheHive Server

Create another Ubuntu 22.04 server for TheHive. Apply the firewall rules you created earlier.

### 6.2 Install Dependencies

```bash
apt install wget gnupg apt-transport-https git ca-certificates ca-certificates-java curl software-properties-common python3-pip lsb-release
```

### 6.3 Install Java

```bash
wget -qO- https://apt.corretto.aws/corretto.key | sudo gpg --dearmor -o /usr/share/keyrings/corretto.gpg
echo "deb [signed-by=/usr/share/keyrings/corretto.gpg] https://apt.corretto.aws stable main" | sudo tee -a /etc/apt/sources.list.d/corretto.sources.list
sudo apt update
sudo apt install java-common java-11-amazon-corretto-jdk
echo JAVA_HOME="/usr/lib/jvm/java-11-amazon-corretto" | sudo tee -a /etc/environment
export JAVA_HOME="/usr/lib/jvm/java-11-amazon-corretto"
```

### 6.4 Install Cassandra

```bash
curl -o /etc/apt/keyrings/apache-cassandra.asc https://downloads.apache.org/cassandra/KEYS
echo "deb [signed-by=/etc/apt/keyrings/apache-cassandra.asc] https://debian.cassandra.apache.org 41x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
sudo apt-get update
sudo apt-get install cassandra
```

### 6.5 Install Elasticsearch

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
sudo apt-get install apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install elasticsearch
```

Optional JVM settings under `/etc/elasticsearch/jvm.options.d`:

```text
-Dlog4j2.formatMsgNoLookups=true
-Xms2g
-Xmx2g
```

### 6.6 Install TheHive

```bash
wget -O- https://archives.strangebee.com/keys/strangebee.gpg | sudo gpg --dearmor -o /usr/share/keyrings/strangebee-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/strangebee-archive-keyring.gpg] https://deb.strangebee.com thehive-5.2 main' | sudo tee -a /etc/apt/sources.list.d/strangebee.list
sudo apt-get update
sudo apt-get install -y thehive
```

Default TheHive credentials:

```text
Username: admin@thehive.local
Password: secret
```

## 7. Configure TheHive Dependencies

**Visual walkthrough: Cassandra, Elasticsearch, and TheHive configuration**

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 21 image 1](../assets/images/page-21-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 22 image 1](../assets/images/page-22-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 22 image 2](../assets/images/page-22-image-02.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 23 image 1](../assets/images/page-23-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 24 image 1](../assets/images/page-24-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 25 image 1](../assets/images/page-25-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 25 image 2](../assets/images/page-25-image-02.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 25 image 3](../assets/images/page-25-image-03.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 26 image 1](../assets/images/page-26-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 27 image 1](../assets/images/page-27-image-01.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 27 image 2](../assets/images/page-27-image-02.png)

![Cassandra, Elasticsearch, and TheHive configuration screenshot page 27 image 3](../assets/images/page-27-image-03.png)


### 7.1 Configure Cassandra

Edit:

```bash
nano /etc/cassandra/cassandra.yaml
```

Update these values to match your TheHive server:

```yaml
cluster_name: "Test Cluster"
listen_address: <THEHIVE_PUBLIC_IP>
rpc_address: <THEHIVE_PUBLIC_IP>
seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
      - seeds: "<THEHIVE_PUBLIC_IP>"
```

Restart Cassandra with fresh package-installed data:

```bash
systemctl stop cassandra.service
rm -rf /var/lib/cassandra/*
systemctl start cassandra.service
systemctl status cassandra.service
```

### 7.2 Configure Elasticsearch

Edit:

```bash
nano /etc/elasticsearch/elasticsearch.yml
```

Common lab settings:

```yaml
cluster.name: Test Cluster
node.name: node-1
network.host: <THEHIVE_PUBLIC_IP>
http.port: 9200
cluster.initial_master_nodes: ["node-1"]
```

Start and enable Elasticsearch:

```bash
systemctl start elasticsearch
systemctl enable elasticsearch
systemctl status elasticsearch
```

### 7.3 Configure TheHive

Check ownership:

```bash
ls -la /opt/thp
chown -R thehive:thehive /opt/thp
```

Edit:

```bash
nano /etc/thehive/application.conf
```

Set the Cassandra hostname, Elasticsearch hostname, cluster name, and application base URL to your lab values.

Then start and enable TheHive:

```bash
systemctl start thehive
systemctl enable thehive
systemctl status thehive
```

Open:

```text
http://<THEHIVE_PUBLIC_IP>:9000/login
```

## 8. Add the Windows Agent to Wazuh

**Visual walkthrough: Wazuh Windows agent onboarding**

![Wazuh Windows agent onboarding screenshot page 28 image 1](../assets/images/page-28-image-01.png)

![Wazuh Windows agent onboarding screenshot page 29 image 1](../assets/images/page-29-image-01.png)

![Wazuh Windows agent onboarding screenshot page 30 image 1](../assets/images/page-30-image-01.png)

![Wazuh Windows agent onboarding screenshot page 30 image 2](../assets/images/page-30-image-02.png)

![Wazuh Windows agent onboarding screenshot page 31 image 1](../assets/images/page-31-image-01.png)

![Wazuh Windows agent onboarding screenshot page 31 image 2](../assets/images/page-31-image-02.png)


In Wazuh:

1. Log in to the Wazuh dashboard.
2. Click **Add agent**.
3. Select **Windows**.
4. Set the server address to `<WAZUH_PUBLIC_IP>`.
5. Copy the generated PowerShell installation command.
6. Run it on the Windows 10 client as Administrator.

Start the Wazuh agent:

```powershell
net start wazuhsvc
```

Confirm the agent shows as `Active`.

## 9. Forward Sysmon Events to Wazuh

**Visual walkthrough: Sysmon forwarding into Wazuh**

![Sysmon forwarding into Wazuh screenshot page 32 image 1](../assets/images/page-32-image-01.png)

![Sysmon forwarding into Wazuh screenshot page 33 image 1](../assets/images/page-33-image-01.png)

![Sysmon forwarding into Wazuh screenshot page 33 image 2](../assets/images/page-33-image-02.png)

![Sysmon forwarding into Wazuh screenshot page 34 image 1](../assets/images/page-34-image-01.png)


On the Windows client, edit:

```text
C:\Program Files (x86)\ossec-agent\ossec.conf
```

Add a Sysmon event channel under the agent configuration:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Optional event channels include PowerShell, Application, Security, and System, but the source lab focuses on Sysmon.

Restart the Wazuh agent:

```powershell
Restart-Service -Name WazuhSvc
```

or:

```powershell
net stop wazuhsvc
net start wazuhsvc
```

Verify Sysmon events in Wazuh Events.

## 10. Generate Detection Telemetry

**Visual walkthrough: Telemetry generation and archive validation**

![Telemetry generation and archive validation screenshot page 35 image 1](../assets/images/page-35-image-01.png)

![Telemetry generation and archive validation screenshot page 36 image 1](../assets/images/page-36-image-01.png)

![Telemetry generation and archive validation screenshot page 36 image 2](../assets/images/page-36-image-02.png)

![Telemetry generation and archive validation screenshot page 37 image 1](../assets/images/page-37-image-01.png)

![Telemetry generation and archive validation screenshot page 38 image 1](../assets/images/page-38-image-01.png)

![Telemetry generation and archive validation screenshot page 38 image 2](../assets/images/page-38-image-02.png)

![Telemetry generation and archive validation screenshot page 39 image 1](../assets/images/page-39-image-01.png)

![Telemetry generation and archive validation screenshot page 39 image 2](../assets/images/page-39-image-02.png)

![Telemetry generation and archive validation screenshot page 40 image 1](../assets/images/page-40-image-01.png)

![Telemetry generation and archive validation screenshot page 40 image 2](../assets/images/page-40-image-02.png)

![Telemetry generation and archive validation screenshot page 41 image 1](../assets/images/page-41-image-01.png)

![Telemetry generation and archive validation screenshot page 41 image 2](../assets/images/page-41-image-02.png)


### 10.1 Generate Mimikatz Telemetry

In the controlled Windows lab machine, generate Mimikatz-related telemetry for detection testing. Keep this isolated and avoid using real credentials.

### 10.2 Enable Wazuh Archive Logging

By default, Wazuh does not archive every event. To troubleshoot and build detections, enable archive logging on the Wazuh manager.

Back up the config:

```bash
cp /var/ossec/etc/ossec.conf ~/ossec-backup.conf
```

Edit:

```bash
nano /var/ossec/etc/ossec.conf
```

Set:

```xml
<logall>yes</logall>
<logall_json>yes</logall_json>
```

Restart Wazuh:

```bash
systemctl restart wazuh-manager.service
```

### 10.3 Enable Filebeat Archive Input

Edit:

```bash
nano /etc/filebeat/filebeat.yml
```

Change the archive input from:

```yaml
enabled: false
```

to:

```yaml
enabled: true
```

Restart Filebeat.

### 10.4 Create the Archive Index

In Wazuh/OpenSearch Dashboards:

1. Go to **Stack Management**.
2. Open **Index Management**.
3. Create an index pattern named:

```text
wazuh-archives-*
```

4. Select `timestamp` as the time field.
5. Use **Discover** to search the new index.

### 10.5 Search for Mimikatz Events

On the Wazuh manager:

```bash
cat /var/ossec/logs/archives/archives.log | grep -i mimikatz
```

If no events appear:

- Confirm Sysmon captured the event.
- Confirm the Wazuh agent is forwarding Sysmon logs.
- Relaunch the telemetry generation in the lab endpoint.

## 11. Create a Custom Wazuh Rule

**Visual walkthrough: Custom Mimikatz detection rule**

![Custom Mimikatz detection rule screenshot page 42 image 1](../assets/images/page-42-image-01.png)

![Custom Mimikatz detection rule screenshot page 42 image 2](../assets/images/page-42-image-02.png)

![Custom Mimikatz detection rule screenshot page 43 image 1](../assets/images/page-43-image-01.png)

![Custom Mimikatz detection rule screenshot page 44 image 1](../assets/images/page-44-image-01.png)

![Custom Mimikatz detection rule screenshot page 45 image 1](../assets/images/page-45-image-01.png)

![Custom Mimikatz detection rule screenshot page 46 image 1](../assets/images/page-46-image-01.png)

![Custom Mimikatz detection rule screenshot page 46 image 2](../assets/images/page-46-image-02.png)

![Custom Mimikatz detection rule screenshot page 47 image 1](../assets/images/page-47-image-01.jpg)

![Custom Mimikatz detection rule screenshot page 47 image 2](../assets/images/page-47-image-02.jpg)


The lab uses the Sysmon `originalFileName` field because the executable can be renamed. Matching `originalFileName` still catches activity when the visible filename changes.

Create or edit the local Wazuh rules file:

```text
local_rules.xml
```

Add:

```xml
<rule id="100002" level="15">
  <if_group>sysmon_event1</if_group>
  <field name="win.eventdata.originalFileName" type="pcre2">(?i)\\mimikatz\.exe</field>
  <description>Mimikatz Usage Detected</description>
  <mitre>
    <id>T1003</id>
  </mitre>
</rule>
```

Restart Wazuh:

```bash
systemctl restart wazuh-manager.service
```

Test by renaming the executable in the Windows lab and regenerating telemetry. The alert should still trigger.

## 12. Send Wazuh Alerts to Shuffle

**Visual walkthrough: Wazuh to Shuffle integration**

![Wazuh to Shuffle integration screenshot page 48 image 1](../assets/images/page-48-image-01.png)

![Wazuh to Shuffle integration screenshot page 48 image 2](../assets/images/page-48-image-02.png)

![Wazuh to Shuffle integration screenshot page 49 image 1](../assets/images/page-49-image-01.png)

![Wazuh to Shuffle integration screenshot page 50 image 1](../assets/images/page-50-image-01.png)

![Wazuh to Shuffle integration screenshot page 50 image 2](../assets/images/page-50-image-02.png)


### 12.1 Create a Shuffle Workflow

In Shuffle:

1. Create an account.
2. Create a new workflow.
3. Add a webhook trigger.
4. Name it something like `Wazuh-Alerts`.
5. Copy the webhook URI.

### 12.2 Configure Wazuh Integration

On the Wazuh manager, edit:

```bash
nano /var/ossec/etc/ossec.conf
```

Add the Shuffle integration:

```xml
<integration>
  <name>shuffle</name>
  <hook_url><SHUFFLE_WEBHOOK_URL></hook_url>
  <rule_id>100002</rule_id>
  <alert_format>json</alert_format>
</integration>
```

The source PDF first shows a broad `<level>3</level>` example, then replaces it with the specific custom rule ID. The specific rule ID is cleaner for this lab because it sends only the Mimikatz detection to Shuffle.

Restart Wazuh:

```bash
systemctl restart wazuh-manager.service
```

Regenerate the lab telemetry and confirm Shuffle receives the alert.

## 13. Build the Shuffle Workflow

**Visual walkthrough: Shuffle enrichment, TheHive alerting, and email notification**

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 51 image 1](../assets/images/page-51-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 52 image 1](../assets/images/page-52-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 52 image 2](../assets/images/page-52-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 53 image 1](../assets/images/page-53-image-01.jpg)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 53 image 2](../assets/images/page-53-image-02.jpg)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 54 image 1](../assets/images/page-54-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 54 image 2](../assets/images/page-54-image-02.jpg)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 55 image 1](../assets/images/page-55-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 55 image 2](../assets/images/page-55-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 56 image 1](../assets/images/page-56-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 56 image 2](../assets/images/page-56-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 57 image 1](../assets/images/page-57-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 58 image 1](../assets/images/page-58-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 58 image 2](../assets/images/page-58-image-02.jpg)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 60 image 1](../assets/images/page-60-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 61 image 1](../assets/images/page-61-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 61 image 2](../assets/images/page-61-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 62 image 1](../assets/images/page-62-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 62 image 2](../assets/images/page-62-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 63 image 1](../assets/images/page-63-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 64 image 1](../assets/images/page-64-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 64 image 2](../assets/images/page-64-image-02.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 65 image 1](../assets/images/page-65-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 66 image 1](../assets/images/page-66-image-01.png)

![Shuffle enrichment, TheHive alerting, and email notification screenshot page 66 image 2](../assets/images/page-66-image-02.jpg)


### 13.1 Extract the SHA256 Hash

In the Shuffle workflow, change the default action to **Regex capture group**.

Input data:

```text
$exec.text.win.eventdata.hashes
```

Regex:

```regex
SHA256=([0-9A-Fa-f]{64})
```

This extracts only the hash value, which is required for a valid VirusTotal query.

### 13.2 Query VirusTotal

1. Create or log in to a VirusTotal account.
2. Copy your API key.
3. In Shuffle, add the VirusTotal app.
4. Authenticate with the API key.
5. Set the VirusTotal `ID` field to the extracted SHA256 value.
6. Save and rerun the workflow.

A successful query should return HTTP `200`.

### 13.3 Prepare TheHive

In TheHive:

1. Log in as `admin@thehive.local`.
2. Create an organization.
3. Create users for the organization.
4. Create a SOAR/integration user for Shuffle.
5. Generate an API key for the Shuffle integration user.
6. Store the API key securely.

### 13.4 Create TheHive Alerts from Shuffle

In Shuffle:

1. Add TheHive app.
2. Authenticate with the TheHive API key.
3. Use:

```text
http://<THEHIVE_PUBLIC_IP>:9000
```

4. Choose the **Create alerts** action.
5. Set a JSON body for the alert.

Example payload:

```json
{
  "description": "Mimikatz Detected on host: DESKTOP-BOBG95",
  "externallink": "",
  "flag": false,
  "pap": 2,
  "severity": "2",
  "source": "Wazuh",
  "sourceRef": "Rule:100002",
  "status": "New",
  "summary": "Details about the Mimikatz detection",
  "tags": [
    "T1003"
  ],
  "title": "Mimikatz Detection Alert",
  "tlp": 2,
  "type": "Internal"
}
```

Save and rerun the workflow. Confirm the alert appears in TheHive.

### 13.5 Enrich the Alert Details

Use Shuffle's **Show Body** output to identify fields from the Wazuh alert. Add useful details to the TheHive summary, such as:

- Hostname.
- Rule ID.
- MITRE technique.
- Command line.
- SHA256 hash.
- VirusTotal detection count.

### 13.6 Send Email Notification

Add an Email app node in Shuffle after enrichment.

Suggested email content:

```text
Subject: SOC Alert - Mimikatz Detected on <HOSTNAME>

Wazuh detected Mimikatz-like telemetry.

Rule: 100002
Technique: T1003
Host: <HOSTNAME>
SHA256: <SHA256>
VirusTotal: <VT_RESULT>
TheHive: <THEHIVE_ALERT_LINK>
```

Save and rerun the workflow. Confirm the analyst email is received.

## 14. Validation Checklist

- [ ] Windows 10 VM is running.
- [ ] Sysmon is installed.
- [ ] Sysmon operational events are visible in Event Viewer.
- [ ] Wazuh server is accessible.
- [ ] Wazuh Windows agent is active.
- [ ] Sysmon events appear in Wazuh.
- [ ] Wazuh archive logging is enabled for troubleshooting.
- [ ] `wazuh-archives-*` index exists.
- [ ] Mimikatz telemetry appears in archive logs.
- [ ] Custom rule `100002` triggers.
- [ ] Wazuh sends matching alerts to Shuffle.
- [ ] Shuffle extracts SHA256 correctly.
- [ ] VirusTotal returns a successful response.
- [ ] TheHive alert is created.
- [ ] Email notification is received.

## 15. Extension Project

The PDF ends with a proposed expansion path for SSH brute-force automation:

1. Create a low-spec Ubuntu machine.
2. Allow inbound traffic for the test scenario.
3. Install a Wazuh agent on Ubuntu.
4. Generate or observe SSH brute-force activity.
5. Push level 5 alerts to Shuffle.
6. Enrich the source IP with VirusTotal.
7. Email the analyst and ask whether to block the IP.
8. Create an alert in TheHive.
9. Automatically block the IP if the analyst confirms.

For safety, keep this extension in a controlled lab and do not expose intentionally weak systems beyond what is necessary for the exercise.

## 16. Final Outcome

At the end of the lab, the SOC workflow should automatically move from endpoint telemetry to alert enrichment and case creation:

```text
Windows Sysmon -> Wazuh custom alert -> Shuffle workflow -> VirusTotal enrichment -> TheHive alert -> Email notification
```

This gives a reusable foundation for automating repetitive SOC triage tasks while keeping the analyst in the loop for investigation and response.
