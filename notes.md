try 1: 6 scrapes at 30 second intervals (180), the last scrape hit the rate limit
-> after the access denied, 3 minute cooldown was not enough to get un-blocked

try 2: 6 scapes per session, randomized wait time 60-90 seconds, with randomized new session wait time of 5-10 minutes, is working

Since the app doesn’t have a traditional website and likely pulls secondary market data directly into the mobile app, here are a few methods you could explore to investigate where it sources its data:

### 1. **Check for an API or Network Calls**
   - **Using a Proxy Tool**: Tools like **Charles Proxy**, **Burp Suite**, or **Wireshark** can intercept network traffic from your phone or iOS simulator. Here’s how to proceed:
      - **Set Up the Proxy**: Configure your device or simulator to route network traffic through the proxy tool.
      - **Inspect HTTP/HTTPS Requests**: Once set up, you can observe the network requests made by the app to see if it accesses specific endpoints or APIs for secondary market data.
      - **Check for JSON Data**: Many apps request JSON data from APIs, which would typically contain structured information about bottle prices and other details.
      - **Note**: Some apps use SSL pinning, which can make it difficult to intercept HTTPS traffic. In such cases, disabling SSL pinning on a rooted or jailbroken device might help (with caution).

### 2. **Reverse Engineering the App**
   - **Decompiling the App**: You can use decompilers or analysis tools like **Ghidra**, **Hopper**, or **JADX** to analyze the app's code and identify potential endpoints or data sources it uses. This process involves examining the app’s structure and code to find references to network calls.
      - **iOS Apps**: iOS apps are compiled into `.ipa` files, which you can open in tools like **Hopper** for static analysis.
      - **Search for API Endpoints**: Look for strings in the app’s code that reference URLs or API endpoints. These endpoints might lead to the external sources or databases that contain the secondary market values.
      - **Note**: Reverse engineering can be complex and may require an understanding of assembly language or decompiled code, depending on the app’s security measures.

### 3. **Automate Interaction with the App to Observe Changes**
   - If you are unable to intercept the network traffic directly, another approach is to automate interaction with the app (using **Appium**, for instance) and observe changes in the data.
      - For example, automate the navigation through different bottle listings or market value screens while capturing data changes to make educated guesses about the data’s origin.
      - This approach is slower but can help you deduce patterns in data updates and price sources.

### 4. **Inspect for External Data Sources on the App’s Backend**
   - **Developer Analysis**: Apps that pull data from a secondary market may rely on an existing data provider for such information. Research common providers of secondary market data in the alcohol and collectibles space, as some of these companies may offer paid APIs or platforms used by similar apps.
   - **App Store Metadata**: Look for clues in the app’s description, terms of service, or privacy policy on the App Store. Sometimes, these documents mention third-party providers or partners that supply the data.

### 5. **Analyze the App’s Update Frequency and Patterns**
   - Track the app’s updates, such as new bottle listings or price changes, to understand the data refresh frequency. Knowing the update frequency can give clues about whether data is scraped in real-time, periodically synced, or statically stored within the app itself.
   
### Important Considerations
- **Legal and Ethical Constraints**: Reverse engineering and intercepting network traffic of an app, especially for proprietary data, might violate terms of service or laws depending on the jurisdiction.
- **Security Protections**: Many apps implement anti-tampering mechanisms, SSL pinning, and data encryption to prevent interception. Bypassing these protections is technically challenging and can require specific skills and tools.

If feasible, the **network traffic interception method** with a proxy tool is generally the most straightforward way to observe data sources without direct access to the app’s backend. It also requires less technical knowledge than reverse engineering and could potentially provide direct insight into the app’s data requests if they’re unencrypted.


Given that your data source for secondary market values is only accessible through an iOS or Google Play app, and you want to compare it to JSON data obtained from a primary market website, here’s a structured approach to collect and compare this data:

### Step 1: Set Up Mobile App Automation for Data Collection

Since you have secondary market data available only in mobile app formats, you’ll need to automate an interaction with the app on either an **iOS simulator** (for iPhone apps) or an **Android emulator** (for Google Play apps). 

#### Option A: Use Appium for Android (Google Play App)
1. **Set Up an Android Emulator**: You can use **Android Studio** to run an emulator on your Mac or PC.
2. **Install Appium**: Appium allows you to automate interactions with Android and iOS apps. Install it on your machine and set up a server.
3. **Locate Key Elements**: Use Appium’s inspector or an Android emulator’s developer tools to find the elements you need within the app (e.g., listings of items, prices, categories).
4. **Extract Data to JSON**: Write a script that interacts with the app and retrieves relevant data (like bottle prices or availability). Format this data as JSON so you can later compare it with primary market data.

#### Option B: Use Appium for iOS (iPhone App)
1. **Set Up an iOS Simulator**: Available through Xcode on Mac. Load the iOS simulator with the app.
2. **Configure Appium for iOS**: Similar to the Android setup, but requires specific configurations for iOS.
3. **Automate Data Collection**: Use accessibility IDs and other identifiers specific to iOS to collect data points within the app, saving the information in JSON format.

### Step 2: Collect JSON Data from the Primary Market Website

For the primary market, if the website provides a JSON-based API or has a traditional front-end you can scrape, proceed with the following:

1. **Scrape or Request JSON Data**: If the website has an API, use it to retrieve JSON data directly. Otherwise, scrape the site’s HTML and parse the data into JSON using libraries like **BeautifulSoup** (for HTML parsing) and **json** in Python.
2. **Save or Clean the Data**: Ensure the JSON format is consistent and contains fields similar to those from the secondary market data for easier comparison.

### Step 3: Normalize and Compare Data

Now that you have JSON data from both sources (secondary market app and primary market website), here’s how to compare it:

1. **Data Normalization**: Align the data fields between both sources so you can make accurate comparisons. For example:
   - **Standardize Field Names**: Ensure that fields like `"price"`, `"name"`, and `"availability"` are uniform in both datasets.
   - **Data Types and Formats**: Make sure values like prices are in a comparable format (e.g., all in USD).

2. **Comparison Script**: Write a script to compare these values. For instance:
   - **Price Difference Calculation**: Calculate the price difference for each item in the secondary and primary markets.
   - **Alerts for Price Anomalies**: If secondary market prices are significantly higher or lower than primary market prices, flag these instances.
   - **Trend Analysis**: If desired, create metrics or trends based on this data, such as average price differences.

### Sample Python Workflow for Comparison

Here’s a Python example that illustrates comparing the two datasets:

```python
import json

# Sample data structure
primary_market_data = [
    {"name": "Bottle A", "price": 100, "availability": "in_stock"},
    {"name": "Bottle B", "price": 150, "availability": "out_of_stock"}
]

secondary_market_data = [
    {"name": "Bottle A", "price": 120, "availability": "limited"},
    {"name": "Bottle B", "price": 180, "availability": "available"}
]

# Comparison function
def compare_markets(primary_data, secondary_data):
    for primary in primary_data:
        for secondary in secondary_data:
            if primary["name"] == secondary["name"]:
                price_difference = secondary["price"] - primary["price"]
                print(f"Item: {primary['name']}")
                print(f"Primary Market Price: ${primary['price']}")
                print(f"Secondary Market Price: ${secondary['price']}")
                print(f"Price Difference: ${price_difference}\n")

# Run comparison
compare_markets(primary_market_data, secondary_market_data)
```

### Summary

1. **Automate the Secondary Market App Data Collection**: Use Appium to scrape relevant data, storing it in JSON format.
2. **Scrape the Primary Market Data**: Use direct API requests or web scraping tools like BeautifulSoup to obtain comparable data from the website.
3. **Normalize and Compare**: Align the data fields and compare metrics like price and availability to gain insights.

This workflow combines mobile app automation and web scraping, allowing you to leverage the secondary market data in real-time alongside traditional primary market data.