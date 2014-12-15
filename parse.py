#Python program for autoconfig wireless network on windows 7/8
import os
import urllib2 as U2
import xml.etree.ElementTree as ET
import plistlib as PL

def parsing():
	WINDOWSoneX = """<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
		<name></name>
		<SSIDConfig>
			<SSID>
				<hex></hex>
				<name></name>
			</SSID>
			<nonBroadcast>true</nonBroadcast>
		</SSIDConfig>
		<connectionType>ESS</connectionType>
		<connectionMode>auto</connectionMode>
		<autoSwitch>false</autoSwitch>
		<MSM>
			<security>
				<authEncryption>
					<authentication>WPA2</authentication>
					<encryption>AES</encryption>
					<useOneX>true</useOneX>
				</authEncryption>
				<sharedKey>
					<keyType>passPhrase</keyType>
					<protected>false</protected>
					<keyMaterial></keyMaterial>
				</sharedKey>
				<OneX xmlns="http://www.microsoft.com/networking/OneX/v1">
					<cacheUserData>true</cacheUserData>
					<authMode>user</authMode>
					<EAPConfig>
						<EapHostConfig xmlns="http://www.microsoft.com/provisioning/EapHostConfig">
							<EapMethod>
								<Type xmlns="http://www.microsoft.com/provisioning/EapCommon">25</Type>
								<VendorId xmlns="http://www.microsoft.com/provisioning/EapCommon">0</VendorId>
								<VendorType xmlns="http://www.microsoft.com/provisioning/EapCommon">0</VendorType>
								<AuthorId xmlns="http://www.microsoft.com/provisioning/EapCommon">0</AuthorId>
							</EapMethod>
							<Config xmlns="http://www.microsoft.com/provisioning/EapHostConfig">
								<Eap xmlns="http://www.microsoft.com/provisioning/BaseEapConnectionPropertiesV1">
									<Type>25</Type>
									<EapType xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV1">
										<ServerValidation>
											<DisableUserPromptForServerValidation>false</DisableUserPromptForServerValidation>
											<ServerNames></ServerNames>
											<TrustedRootCA>df 72 a6 7b b9 f5 9a 61 96 68 f5 b8 da ca 36 76 21 84 98 ec </TrustedRootCA>
										</ServerValidation>
										<FastReconnect>true</FastReconnect>
										<InnerEapOptional>false</InnerEapOptional>
										<Eap xmlns="http://www.microsoft.com/provisioning/BaseEapConnectionPropertiesV1">
											<Type>26</Type>
											<EapType xmlns="http://www.microsoft.com/provisioning/MsChapV2ConnectionPropertiesV1">
												<UseWinLogonCredentials>false</UseWinLogonCredentials>
											</EapType>
										</Eap>
										<EnableQuarantineChecks>false</EnableQuarantineChecks>
										<RequireCryptoBinding>false</RequireCryptoBinding>
										<PeapExtensions>
											<PerformServerValidation xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV2">true</PerformServerValidation>
											<AcceptServerName xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV2">false</AcceptServerName>
											<PeapExtensionsV2 xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV2">
												<AllowPromptingWhenServerCANotFound xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV3">true</AllowPromptingWhenServerCANotFound>
											</PeapExtensionsV2>
										</PeapExtensions>
									</EapType>
								</Eap>
							</Config>
						</EapHostConfig>
					</EAPConfig>
				</OneX>
			</security>
		</MSM>
	</WLANProfile>
	"""
	WINDOWSopen = """<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
		<name></name>
		<SSIDConfig>
			<SSID>
				<hex></hex>
				<name></name>
			</SSID>
			<nonBroadcast>false</nonBroadcast>
		</SSIDConfig>
		<connectionType>ESS</connectionType>
		<connectionMode>manual</connectionMode>
		<autoSwitch>false</autoSwitch>
		<MSM>
			<security>
				<authEncryption>
					<authentication>WPA2PSK</authentication>
					<encryption>AES</encryption>
					<useOneX>false</useOneX>
					<FIPSMode xmlns="http://www.microsoft.com/networking/WLAN/profile/v2">false</FIPSMode>
				</authEncryption>
				<sharedKey>
					<keyType>passPhrase</keyType>
					<protected>false</protected>
					<keyMaterial>Inverseforthewin!</keyMaterial>
				</sharedKey>
			</security>
		</MSM>
	</WLANProfile>"""
	
	#Download mobileconfig file, convert to str
	origin = U2.urlopen("https://packetfence.org/wireless-profile.mobileconfig") 
	data = origin.read()
	
	#Get data from the mobileconfig file, ssidname, security type, password, profile name, certificate
	r = PL.readPlistFromString(data)
	ssidn = r["PayloadContent"][0]["SSID_STR"]
	sec = r["PayloadContent"][0]["EncryptionType"]
	profile = r["PayloadDisplayName"]
	passk = r["PayloadContent"][0]["Password"]
	#certn = r["PayloadContent"][1]["PayloadCertificateFileName"]
	#certd = r["PayloadContent"][1]["PayloadContent"]
	#certt = r["PayloadContent"][1]["PayloadType"]
	
  #Security of the SSID
	if "EAPClientConfiguration" in r:
		un = r["PayloadContent"][0]["EAPClientConfiguration"]["UserName"]
		eap = r["PayloadContent"][0]["EAPClientConfiguration"]["AcceptEAPTypes"][0]
		root = ET.fromstring(WINDOWSoneX)
		enc = root.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}MSM/{http://www.microsoft.com/networking/WLAN/profile/v1}security/{http://www.microsoft.com/networking/WLAN/profile/v1}authEncryption/{http://www.microsoft.com/networking/WLAN/profile/v1}encryption")[0]
		if sec == "WPA":
			sec = "WPA2"
			enc.text = "AES"
		elif sec == "WEP":
			sec = "WEP"
			enc.text = "WEP"
 	else:
  	root = ET.fromstring(WINDOWSopen)
    enc = root.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}MSM/{http://www.microsoft.com/networking/WLAN/profile/v1}security/{http://www.microsoft.com/networking/WLAN/profile/v1}authEncryption/{http://www.microsoft.com/networking/WLAN/profile/v1}encryption")[0]
		if sec == "WEP":
			sec = "WEP"
			enc.text = "WEP"
		elif sec == "WPA":
			sec = "WPA2PSK"
			enc.text = "AES"
		else:
			sec = "open"
			enc.text = "none"

	#Insert certificate

	#Search specific fields in wintemplate and remplace it
	nname = root.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}name")[0]
	nname.text = profile
	ssid = root.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}SSIDConfig/{http://www.microsoft.com/networking/WLAN/profile/v1}SSID")[0]
	name = ssid.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}name")[0]
	name.text = ssidn
	hexname = ssid.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}hex")[0]
	hexname.text = ssidn.encode("hex")  
	secf = root.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}MSM/{http://www.microsoft.com/networking/WLAN/profile/v1}security")[0]
	sect = secf.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}authEncryption/{http://www.microsoft.com/networking/WLAN/profile/v1}authentication")[0]
	sect.text = sec
	passw = secf.findall("{http://www.microsoft.com/networking/WLAN/profile/v1}sharedKey/{http://www.microsoft.com/networking/WLAN/profile/v1}keyMaterial")[0]
	passw.text = passk
	
	
	#Get the path to temp folder(right to write)
	pa = os.getenv("tmp")
	file = os.path.join(pa, "template-out.xml")

	config = ET.tostring(root) 

	#Create new file with data 
	with open(file, "w") as configfile:
		configfile.write(config)	

	#Win command to add wifi profile
	net = "netsh wlan add profile filename="
	os.system(net+file)

	#Remove config file
	df = "del /F "
	os.system(df+file)
 
#  Copyright (C) 2005-2014 Inverse inc.
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
#  USA.
