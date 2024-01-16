from playwright.sync_api import sync_playwright
import uuid
import validators
import playwright

def main():
    try:
        link = ""
        download_from_file = input("Do you want to download video from a file? (yes/no): ")
        def process_link(link: str, output_directory: str) -> None:
            # Launch the browser
            print("Launching the browser...")
            browser = playwright.firefox.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Go to the target website
            page.goto("https://publer.io/tools/media-downloader")

            # Fill in the link input field
            page.get_by_placeholder("https://").click()
            page.get_by_placeholder("https://").fill(link)

            # Click the download button
            page.get_by_role("button", name="Download").click()

            # Wait for the download to complete
            with page.expect_download() as download_info:
                page.get_by_text("Download to your device").click()
            download = download_info.value

            output_file = f"{output_directory}/{uuid.uuid4()}.mov"

            # Save the downloaded file
            download.save_as(output_file)
            print("Saved as:", output_file)

            # Close the browser
            context.close()
            browser.close()
            print("Browser closed")

        if download_from_file.lower() == "yes":
            file_path = input("Enter the file path: ")
            output_directory = input("Enter the output directory: ")
            with open(file_path, "r") as file:
                links = file.readlines()
                link_count = 0
                for link in links:
                    link = link.strip()
                    if validators.url(link):
                        print(f"Valid link: {link}")
                        link_count += 1
                        process_link(link, output_directory)
                    else:
                        print(f"Invalid link: {link}")
        else:
            link = input("Enter the link: ")
            output_directory = input("Enter the output directory: ")
            if validators.url(link):
                print(f"Valid link: {link}")
                process_link(link, output_directory)
            else:
                print(f"Invalid link: {link}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit()

if __name__ == "__main__":
    main()