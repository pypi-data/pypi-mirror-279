# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import os
from urllib import parse as urlparse
from urllib.request import (
    HTTPBasicAuthHandler,
    HTTPPasswordMgrWithDefaultRealm,
    build_opener,
)

import requests


def replacement_func(url):
    """A function for making a an id from catalog URL for collections"""
    split_arr = urlparse.urlsplit(url)
    trans_dict_path = {"%": "", "/catalog.xml": "", "/thredds/": "", "/": " "}
    path_ = split_arr.path
    query_ = split_arr.query
    for k, v in trans_dict_path.items():
        temp = path_.split(k)
        path_ = v.join(temp)
    if split_arr.query != "":
        trans_dict_query = {"=": " ", "?": " ", "/": " "}
        for k, v in trans_dict_query.items():
            temp = query_.split(k)
            query_ = v.join(temp)
        replaced_url = path_.replace(".xml", "") + " " + query_
        trans_dict_replaced = {".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    else:
        replaced_url = path_
        trans_dict_replaced = {".xml": "", ".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    replaced_url = replaced_url.replace(".", " ")
    return replaced_url.title()


def replacement_func_collection_item_id(url):
    """A function for making a an id from catalog URL for collections"""
    split_arr = urlparse.urlsplit(url)
    trans_dict_path = {"%": "", "/catalog.xml": "", "/thredds/": "", "/": " "}
    path_ = split_arr.path
    query_ = split_arr.query
    for k, v in trans_dict_path.items():
        temp = path_.split(k)
        path_ = v.join(temp)
    if split_arr.query != "":
        trans_dict_query = {"=": " ", "?": " ", "/": " "}
        for k, v in trans_dict_query.items():
            temp = query_.split(k)
            query_ = v.join(temp)
        replaced_url = path_.replace(".xml", "") + " " + query_
        trans_dict_replaced = {".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    else:
        replaced_url = path_
        trans_dict_replaced = {".xml": "", ".nc": "", "-": " ", "_": " "}
        for k, v in trans_dict_replaced.items():
            temp = replaced_url.split(k)
            replaced_url = v.join(temp)
    replaced_url = replaced_url.lower()
    replaced_url = replaced_url.replace(" ", "_")
    replaced_url = replaced_url.replace(".", "_")
    return replaced_url


def html2xml(url):
    """A function for making a an xml URL from html URL"""
    u = urlparse.urlsplit(url)
    path, extension = os.path.splitext(u.path)
    if extension == ".html":
        u = urlparse.urlsplit(url.replace(".html", ".xml"))
    return u.geturl()


def xml2html(url):
    """A function for making a an html URL from xml URL"""
    u = urlparse.urlsplit(url)
    path, extension = os.path.splitext(u.path)
    if extension == ".xml":
        u = urlparse.urlsplit(url.replace(".xml", ".html"))
    return u.geturl()


def get_xml(url, request_properties):
    """A function for getting XML content from url"""

    try:
        if request_properties is not None and request_properties != {}:
            xml_url = requests.get(
                url,
                None,
                auth=request_properties["auth"],
                verify=request_properties["verify"],
                timeout=request_properties["timeout"],
            )
            xml = xml_url.text.encode("utf-8")
            return xml
        else:
            xml_url = requests.get(url)
            xml = xml_url.text.encode("utf-8")
            return xml
    except BaseException:
        pass
        return None


def references_urls(url, additional):
    split_arr = urlparse.urlsplit(url)
    common_url = str(split_arr.scheme) + "://" + str(split_arr.netloc)
    without_catalog_xml = urlparse.urljoin(
        common_url, os.path.split(split_arr.path)[0]
    )

    if not additional:
        final_url = url
    elif additional[:4] == "http":
        # finding http or https
        final_url = additional
    elif additional[0] == "/":
        # Absolute paths
        final_url = urlparse.urljoin(common_url, additional)
    else:
        # Relative paths.
        final_url = without_catalog_xml + "/" + additional
    return final_url


def xml_processing(catalog, request_properties):
    """A function for getting out XML details of a catalog URL"""
    catalog_xml = html2xml(catalog)
    catalog_id = replacement_func(catalog_xml)
    xml_final = get_xml(catalog_xml, request_properties)
    return catalog_xml, catalog_id, xml_final


def xml_tag_name_ncml(input_xml, var_name):
    """A function for finding the tag names in NcML XML files"""

    # A list for recognizign the exceptions.
    # This list contains variable's name with same `input_xml.tag` and different `var_name`s
    exception_list = ["var_lists", "var_dims", "var_descs", "keyword"]

    if var_name in exception_list:
        return input_xml.tag + "_" + var_name
    else:
        return str(input_xml.get("name")) + "_" + var_name


def xml_tag_finder(input_xml, web_service, var_name):
    """A function for finding the tag names in all TDS webservices"""

    tag_finder_dict = {
        "iso": input_xml.tag + "_" + var_name,
        "ncml": xml_tag_name_ncml(input_xml, var_name),
        "wms": input_xml.tag + "_" + var_name,
    }

    return tag_finder_dict.get(
        web_service,
    )


def validate_catalog_url(url, requests_properties):
    """A function for validating the catalog URL"""
    try:
        if requests_properties is not None and requests_properties != {}:
            xml_url = requests.get(
                url,
                None,
                auth=requests_properties["auth"],
                verify=requests_properties["verify"],
                timeout=requests_properties["timeout"],
            )
            if xml_url.status_code == 200:
                return True
            else:
                return False
        else:
            xml_url = requests.get(url)
            if xml_url.status_code == 200:
                return True
            else:
                return False
    except BaseException:
        return False


def merge_bboxes(bbox1, bbox2):
    x1_1, y1_1, x2_1, y2_1 = bbox1
    x1_2, y1_2, x2_2, y2_2 = bbox2
    new_x1 = min(x1_1, x1_2)
    new_y1 = min(y1_1, y1_2)
    new_x2 = max(x2_1, x2_2)
    new_y2 = max(y2_1, y2_2)
    return (new_x1, new_y1, new_x2, new_y2)


def merge_intervals(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    merged_start = min(start1, start2)
    merged_end = max(end1, end2)
    return (merged_start, merged_end)


def opener_module(service_url, requests_properties):
    # Set your URL, username, and password

    username = requests_properties["auth"][0]
    password = requests_properties["auth"][1]
    # Create a password manager
    password_mgr = HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, service_url, username, password)

    # Create an opener that will replace the default urlopen method on further calls
    handler = HTTPBasicAuthHandler(password_mgr)
    opener = build_opener(handler)
    opener.open(service_url)
