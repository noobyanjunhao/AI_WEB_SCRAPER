import screenshot_taker

#test for fill in zip code in popup
from selenium import webdriver

screenshot_taker.fill_zip_code_generic(
    driver,
    zip_code="10001",
    input_xpath='//*[@id="pie-store-finder-modal-search-field"]',
    button_selector="#sf-search-icon"
)
        