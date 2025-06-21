# Sending SMSs from a PC, via an android mobile phone, using pre-defined messages and pre-defined groups

This application is a PC client GUI of "SMS Gateway" application running on an Android mobile phone.
It fires up http requests against a mobile phone.
The mobile app was taken from
https://sms-gate.app/
https://github.com/capcom6/android-sms-gateway
It was tested against version 1.34.0

## Packaging the application, producing an exe file (python is not required to be installed at the machone running the app)

At the top level folder, execute packager.bat
It will generate an exe file under dist folder


## Prerequisites

* **Python 3.x** installed on your system.
* The **requests** library. You can install it using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Installation

1.  Save the Python code provided (e.g., as `api_gui.py`).
2.  Create a file named `requirements.txt` in the same directory as the Python script.
3.  Add the following line to `requirements.txt`:

    ```
    requests
    ```
4.  Open your terminal or command prompt, navigate to the directory where you saved the files, and run the installation command:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the Python script from your terminal:

    ```bash
    python api_gui.py
    ```

2.  A window titled "Text Input and API Call" will appear.

3.  **Enter Text:** Type any text you want to send to the API in the multiline text field.

4.  **Select Option:** Choose an option from the dropdown menu.

5.  **Call API:** Click the "Call API" button.

6.  The script will then:
    * Display "Calling API..." below the button.
    * Make a POST request to `https://httpbin.org/post` (this is a test endpoint; **you should replace it with your actual API URL in the `call_api` function**).
    * Display the JSON response received from the API below the button.
    * If there is an error during the API call, an error message will be displayed instead.

## Code Structure

* **`call_api(text_content, selected_option, output_label)`:** This function is responsible for making the HTTP POST request. It takes the text input, the selected dropdown option, and the label for displaying output as arguments. It sends the data as a JSON payload to the `api_url` and updates the `output_label` with the API's response or any error. It runs in a separate thread to prevent the GUI from freezing.
* **`on_button_click()`:** This function is called when the "Call API" button is clicked. It retrieves the text from the text field and the selected option from the dropdown, updates the output label to indicate the API call is in progress, and then starts a new thread to execute the `call_api` function.
* The main part of the script creates the Tkinter window and the GUI elements: a label and text field for input, a label and Combobox for the dropdown, a button to trigger the API call, and a label to display the output.

## Important Notes

* **Replace the API URL:** In the `call_api` function, the `api_url` is currently set to `"https://httpbin.org/post"`. **You must change this to the actual URL of the API endpoint you want to interact with.**
* **API Interaction:** The script currently sends a POST request with the text and dropdown value as a JSON payload. You may need to adjust the HTTP method (e.g., GET, PUT, DELETE) and the structure of the data sent to match the requirements of your API.
* **Error Handling:** The script includes basic error handling for network-related issues during the API call. You might want to add more specific error handling based on the possible responses from your API.
* **GUI Layout:** The GUI elements are arranged using the `.pack()` method. You can explore other layout managers like `.grid()` or `.place()` for more complex and precise UI designs.
