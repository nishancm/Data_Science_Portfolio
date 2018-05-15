import time
from selenium import webdriver


def get_job_url(job_title, need):
    """
    Get URLs of indeed resumes for a given job title
        until the required number resumes (need) is met
    :param job_title: job title interested
    :param need: number of resumes needed
    :return: URLs as a list
    """
    links = set()  # to avoid duplicates
    driver = get_title(job_title)
    time.sleep(2)  # don't call next driver function before loading

    while len(links) < need:
        links = links.union(get_urls(driver))
        next_page(driver)

    driver.close()
    return links


def get_title(job_title):
    """
    Navigate to the main web page for a given job
        title in indeed for US candidates
    :param job_title: job title interested
    :return: Google chrome driver object after navigation
    """
    driver = webdriver.Chrome()  # '/usr/local/bin/chromedriver')
    driver.get('https://resumes.indeed.com')
    title = driver.find_element_by_name('q')  # find text box to enter title
    title.clear()  # clear text box
    title.send_keys(job_title)

    where = driver.find_element_by_name('l')
    where.clear()
    where.send_keys('United States')  # only interested in resumes from US
    where.submit()
    return driver


def get_urls(driver):
    """
    Find all URLs for resumes in a given webpage
    :param driver: Google chrome driver
    :return: URLs as a list
    """
    clients = driver.find_elements_by_class_name(
        'rezemp-u-h4')  # point to resumes
    links = [s.get_attribute('href') for s in clients]  # resume links

    return links


def next_page(driver):
    """
    Go to next web page containing resumes
    :param driver: Google chrome driver
    :return: None
    """
    next_ = ".icl-TextLink.icl-TextLink--primary.rezemp-pagination-nextbutton"
    next_page = driver.find_element_by_css_selector(next_)
    next_page.click()


def write_url_file(job_title, urls):
    """
    Write all resume URLs extracted for given job title in to a file
    :param job_title: job title interested
    :param urls: All URLs extracted as a list
    :return: None
    """
    with open('Data/Profile_URLs/' + job_title + '.txt', 'w') as f:
        for u in urls:
            f.write('%s\n' % u)


if __name__ == '__main__':
    job_titles = [
        'Data Scientist',
        'Data Analyst',
        'Data Engineer',
        'Software Engineer',
        'Business Analyst',
        'Product Manager',
        'VP of Engineering',
        'VP of Marketing',
        'Financial Analyst',
        'Business Strategist',
        'Engineering Manager',
        'Sales Manager',
        'Finance Manager',
        'Sales Associate',
        'Operation Analyst',
        'VP of Operations',
        'Operation Manager',
        'Architect',
        'Software Architect',
        'Human Resource Manager',
        'Recruiter',
        'Marketing Director',
        'Auditor']

    need = 500
    for jt in job_titles:
        urls = get_job_url(jt, need)
        write_url_file(jt, urls)
