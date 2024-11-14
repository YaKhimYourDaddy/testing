import asyncio
import time
import pandas as pd
from playwright.async_api import async_playwright

# Đọc dữ liệu từ file Excel
def read_test_data(file_path):
    data = pd.read_excel(file_path)
    return data

# Ghi kết quả test vào file Excel
def write_test_results(file_path, results):
    results_df = pd.DataFrame(results)
    results_df.to_excel(file_path, index=False)

# Hàm thực hiện test Sign Up
async def test_signup(playwright, data):
    results = []
    for index, row in data.iterrows():
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        # stealth_sync(page)
        await page.goto("https://phptravels.net/signup")

        # with recaptchav2.SyncSolver(page) as solver:
            # token = solver.solve_recaptcha(wait=True, image_challenge=True)
            # print(token)
            
        # Điền thông tin từ Excel
        await page.fill("input[name='first_name']", row['FirstName'])
        await page.fill("input[name='last_name']", row['LastName'])
        await page.get_by_title("Select Country").click()
        await page.fill("input[aria-label='Search']", row['Country'])
        await page.keyboard.press("Enter")
        await page.fill("input[name='phone']", str(row['Phone']))
        await page.fill("input[name='user_email']", row['Email'])
        await page.fill("input[name='password']", row['Password'])
            
            
            
        # if row['Expect'] == "Successful":
        #     if is_enabled == True:
        #         print("true")
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Passed"})
        #     else:
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Failed"})

        # await page.click("button[type='submit']")
        # is_reload = await page.wait_for_load_state('load', timeout=5000)
        # is_navigated = await page.wait_for_url("https://phptravels.net/signup_success", timeout=5000)
        # if row['Expect'] == "Already Exist":
        #     if is_reload == True:
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Passed"})
        #     else:
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Failed"})
        # if row['Expect'] == "Successful":
        #     if is_navigated == True:
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Passed"})
        #     else:
        #         results.append({"Test Case": f"Sign Up {index+1}", "Result": "Failed"})
    # browser.close()
    return results

# Hàm thực hiện test Login
async def test_login(playwright, data):
    results = []
    for index, row in data.iterrows():
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        await page.goto("https://phptravels.net/login")
        
        # Điền thông tin từ Excel
        time.sleep(1)
        await page.fill("input[name='email']", row['Email'])
        time.sleep(1)
        await page.fill("input[name='password']", row['Password'])
        
        # Submit form
        time.sleep(1)
        await page.click("button[type='submit']")
        
        # Chờ kết quả và ghi lại kết quả test
        try:
            await page.wait_for_url("https://phptravels.net/dashboard", timeout=5000)
            results.append({"Test Case": f"Login {index+1}", "Result": "Passed"})
        except Exception:
            results.append({"Test Case": f"Login {index+1}", "Result": "Failed"})
        time.sleep(1)
    # browser.close()
    return results

async def main():
    # Đường dẫn tới file Excel chứa dữ liệu test
    input_signup_file = "signup_test_data.xlsx"
    output_signup_file = "signup_test_results.xlsx"
    input_login_file = "login_test_data.xlsx"
    output_login_file = "login_test_results.xlsx"
    # Đọc dữ liệu test
    input_signup_data = read_test_data(input_signup_file)
    input_login_file = read_test_data(input_login_file)
    
    async with async_playwright() as playwright:
        signup_results = await test_signup(playwright, input_signup_data)
        login_results = await test_login(playwright, input_signup_data)
        
        # Ghi kết quả test ra file Excel
        await write_test_results(output_signup_file, signup_results)
        await write_test_results(output_login_file, login_results)
    
    await print("Test hoàn thành. Kết quả đã được lưu vào file test_results.xlsx.")


if __name__ == "__main__":
    asyncio.run(main())
