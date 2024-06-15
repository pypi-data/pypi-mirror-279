# coding=utf-8
"""
Definition for the types used in this module:
- GrabResult: enum for the result of grabbing a page
- UEAssetType: enum to represent the asset type
- DataSourceType: an enum to represent the data source type
- WidgetType: enum for the widget types.
"""
from enum import Enum


class GrabResult(Enum):
    """
    Enum for the result of grabbing a page.
    """
    NO_ERROR = 0
    # next codes could occur only with beautifulsoup data grabbing (UEVM Version 1.X.X.X)
    INCONSISTANT_DATA = 1
    PAGE_NOT_FOUND = 2
    CONTENT_NOT_FOUND = 3
    TIMEOUT = 4
    # next codes could occur only with API scraping only (UEVM version 2.X.X.X)
    PARTIAL = 5  # when asset has been added when owned asset data only (less complete that "standard" asset data)
    NO_APPID = 6  # no appid found in the data (will produce a file name like '_no_appId_asset_1e10acc0cca34d5c8ff7f0ab57e7f89f
    NO_RESPONSE = 7  # the url does not return HTTP 200


class DataFrameUsed(Enum):
    """ Enum to represent the data frame used for getting or setting the data"""
    AUTO = 0  # Automatically select the data frame wether it is filtered or not
    UNFILTERED = 1  # Use the data frame with unfiltered data
    FILTERED = 2  # Use the data frame with filtered data
    MODEL = 3  # Use the model.df.
    BOTH = 4  # Use both data frames


class UEAssetType(Enum):
    """ Enum to represent the asset type """
    Unknown = 0
    Plugin = 1
    Asset = 2
    Manifest = 3

    @property
    def category_name(self):
        """ Return the category name of the asset type """
        if self == self.Plugin:
            return 'local/plugins'  # existing category in the marketplace
        if self == self.Asset:
            return 'local/asset'  # non-existing category in the marketplace
        if self == self.Manifest:
            return 'local/manifest'  # non-existing category in the marketplace
        return 'local/unknown'  # non-existing category in the marketplace


class DataSourceType(Enum):
    """ Enum to represent the data source type """
    FILE = 1
    SQLITE = 2


class WidgetType(Enum):
    """ Enum for the widget types """
    ENTRY = 0  # Entry widget
    TEXT = 1  # Text widget
    LABEL = 2  # Label widget
    CHECKBUTTON = 3  # Checkbutton widget
    BUTTON = 4  # Button widget
