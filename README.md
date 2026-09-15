# LinkArmor Prototype

A college-project prototype for detecting common suspicious URL indicators.

## Run
1. Install Python 3.
2. Open a terminal in this folder.
3. Run:
   pip install flask
4. Run:
   python app.py
5. On the computer, find its local IPv4 address with `ipconfig` (for example, `192.168.1.25`).
6. Connect the phone and computer to the same Wi-Fi network, then open `http://YOUR_IPV4_ADDRESS:5000` on the phone (for example, `http://192.168.1.25:5000`).

If Windows Firewall asks whether Python can communicate on the network, allow it on **Private networks**. Keep the terminal running while using the phone.

## Demo
Use the built-in harmless examples. Do not visit real phishing websites.

## Important
This is a heuristic demonstration, not a production anti-phishing system. A production system would need reputation feeds, DNS/domain intelligence, safe browsing checks, stronger URL parsing, logging, privacy controls, and extensive testing.
