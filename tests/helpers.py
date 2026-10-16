"""This is where helper functions are located"""

def status_code_with_message(self, response):
    """creates a test_protocol.log file whose contents show whether a test worked or not, similar to 'Postman'"""
    with open("test_protocol.log", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("-" * 160 + "\n")
        f.write(f"Test: {self._testMethodName}\n")
        f.write(is_it_successful(self, response))
        f.write(f"Status: {response.status_code}\n")
        f.write(f"Response: {response.data} \n")
        f.write(customized_cookie_output(response))
        f.write("-" * 160 + "\n")

def is_it_successful(self, response):
    """checks whether the test could be processed, was a success or was a failure"""
    method_name_number = self._testMethodName.split("_")[-1]
    code = int(method_name_number) if method_name_number.isdecimal() else None

    if code == None:
        return "Integer not found, or in the wrong position 🟠\n"

    elif code == response.status_code:
        return "Test successful: Yes 🟢\n"

    elif code != response.status_code and code != None:
        return "Test successful: No 🔴\n"

def customized_cookie_output(response):
    """This function will issue cookies if there are any"""
    cookies = response.cookies
    output = ""

    if len(cookies) > 0:
        index = 1
        output = "Cookies:\n"

    for cookie in cookies:
        output += f"\t{index}. Cookie "
        output += f"({cookies.get(cookie).key}): {cookies.get(cookie).value}\n"
        index += 1

    return output