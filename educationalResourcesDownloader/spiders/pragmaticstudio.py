from typing import Iterable
from scrapy import Spider
from scrapy.http import Request, Response, FormRequest
import os

from ..items import EducationalresourcesdownloaderItem


class pragmaticStudio(Spider):
    name = "pragmaticstudio"

    baseUrl = "https://online.pragmaticstudio.com"

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url="https://pragmaticstudio.com/signin",
            callback=self.login,
        )

    def login(self, response: Response) -> Iterable[Request]:
        authTokenSelector = "input[name='authenticity_token']"
        login = input("login: ")
        password = input("pass: ")

        yield FormRequest.from_response(
            response=response,
            formcss=authTokenSelector,
            formdata={"email": login, "password": password},
            callback=self.after_login,
        )

    def after_login(self, response: Response) -> Iterable[Request]:
        yield Request(url=f"{self.baseUrl}/courses", callback=self.extractCourseInfo)

    def extractCourseInfo(self, response: Response):
        courses = response.css(".md\:space-y-0")

        for course in courses:
            item = EducationalresourcesdownloaderItem()

            item["name"] = course.css(".text-zinc-800::text").get().strip()
            item["edition"] = course.css(".font-medium::text").get().strip()
            item["cover"] = course.css(".border-tan-300::attr(src)").get()

            self.logger.info(item)
            print(item["name"])

            coursePath = os.path.join(
                os.getcwd(), "courses", "pragmatic", item["name"].replace("/", "_")
            )

            if not os.path.exists(coursePath):
                os.makedirs(coursePath)

            yield item
            yield Request(
                url=f"{self.baseUrl}/courses/elixir/downloads",
                callback=self.extractVideo,
                cb_kwargs={"path": coursePath},
            )

    def extractVideo(self, response: Response, path) -> Iterable[Request]:
        tableRows = response.css("table tr")

        for row in tableRows:
            downloadTitle = row.css("td::text").get().strip()
            downloadUrl = row.css("a::attr(href)").get()

            yield Request(
                url=f"{self.baseUrl}{downloadUrl}",
                callback=self.saveVideo,
                cb_kwargs={"downloadTitle": downloadTitle, "path": path},
            )

    # TODO: Ta horrivel, melhorar kkk
    def saveVideo(self, response: Response, downloadTitle, path):
        with open(f"{path}/{downloadTitle}" + ".zip", "wb") as f:
            f.write(response.body)
