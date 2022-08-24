#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
from random import randint
from time import sleep

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

DAY_START = datetime.strptime('07:00', '%H:%M')
DAY_START_VARIATION = 60  # in minutes
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri']


def generate_times():
    variation = randint(-DAY_START_VARIATION, DAY_START_VARIATION)
    start = DAY_START + timedelta(minutes=variation)
    break_start = start + timedelta(hours=4)
    break_end = break_start + timedelta(hours=1)
    end = break_end + timedelta(hours=4)
    start_str = start.strftime('%H:%M AM')
    end_str = end.strftime('%H:%M')
    break_start_str = break_start.strftime('%H:%M')
    break_end_str = break_end.strftime('%H:%M')
    return start_str, break_start_str, break_end_str, end_str


def dayint(day):
    try:
        return int(day)
    except ValueError:
        return DAYS.index(day.lower())


def main():
    parser = argparse.ArgumentParser(
        description="Workday timesheet helper"
    )

    parser.add_argument(
        "-w",
        "--week",
        dest="week",
        default=None,
        type=int,
        help="Week to fill timesheet for [number]",
    )

    parser.add_argument(
        "-s",
        "--skip",
        dest="skip",
        default=None,
        help="Comma-separated list of days to skip (Monday==0 or mon)",
    )

    args = parser.parse_args()

    now = datetime.now()
    week = args.week

    if not week:
        year, week, _ = now.isocalendar()
        print("WARNING: Week not specified, using the current one")

    first_day_of_week = datetime.strptime(f'{now.year}-{week-1}-1', "%Y-%U-%w").date()

    print(f"Week: {week}, monday: {first_day_of_week}")

    if args.skip:
        days_to_skip = [dayint(d.strip()) for d in args.skip.split(",")]
        days_titles = ", ".join(DAYS[i].title() for i in days_to_skip)
        print(f"Days to skip: {days_titles}")
    else:
        days_to_skip = []

    br = webdriver.Firefox()
    br.implicitly_wait(2)
    wait = ui.WebDriverWait(br, 60)

    br.get('https://rover.redhat.com/apps/')

    link_to_wd = br.find_element("xpath", "//a[contains(@title, 'Performance & development, career management, onboarding, compensation, and more.')]")
    link_to_wd.click()

    sleep(3)

    br.switch_to.window(br.window_handles[-1])

    wait.until(ec.element_to_be_clickable((By.XPATH, "//div[@title='Time']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@title='Select Week']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[contains(@id, 'input')]"))).send_keys(str(first_day_of_week.month).zfill(2) + str(first_day_of_week.day).zfill(2) + str(first_day_of_week.year))
    wait.until(ec.element_to_be_clickable((By.XPATH, "//span[@title='OK']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//span[@title='Actions']"))).click()
    sleep(1)
    wait.until(ec.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Quick Add')]"))).click()
    sleep(2)
    wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@title='Next']"))).click()
    wait.until(ec.element_to_be_clickable((By.XPATH, "//span[@title='Add']"))).click()
    sleep(1)
    inputs = br.find_elements("xpath", "//input[@type='text']")

    times = generate_times()

    for input, time in zip(inputs[:4], times):
        input.send_keys(time)

    br.find_element("xpath", "//div[@data-automation-id='selectShowAll']").click()

    br.find_element("xpath", "//div[@title='Break']").click()

    days = br.find_elements("xpath", "//div[@data-automation-id='checkboxPanel']")

    for index, day in enumerate(days[:-2]):
        if index in days_to_skip:
            continue
        day.click()

    br.find_element("xpath", "//button[@title='OK']").click()


if __name__ == "__main__":
    main()
