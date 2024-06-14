# -*- coding: utf-8 -*-
#
# This class was auto-generated.
#
from onlinepayments.sdk.data_object import DataObject


class RateDetails(DataObject):
    __exchange_rate = None
    __inverted_exchange_rate = None
    __mark_up_rate = None
    __quotation_date_time = None
    __source = None

    @property
    def exchange_rate(self) -> float:
        """
        | Expressed as a percentage, applied to convert the original amount into the resulting amount without charge

        Type: float
        """
        return self.__exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, value: float):
        self.__exchange_rate = value

    @property
    def inverted_exchange_rate(self) -> float:
        """
        | Exchange rate, expressed as a percentage, applied to convert the resulting amount into the original amount

        Type: float
        """
        return self.__inverted_exchange_rate

    @inverted_exchange_rate.setter
    def inverted_exchange_rate(self, value: float):
        self.__inverted_exchange_rate = value

    @property
    def mark_up_rate(self) -> float:
        """
        | The markup is the percentage added to the exchange rate by a provider when they sell you currency.

        Type: float
        """
        return self.__mark_up_rate

    @mark_up_rate.setter
    def mark_up_rate(self, value: float):
        self.__mark_up_rate = value

    @property
    def quotation_date_time(self) -> str:
        """
        | Date and time at which the exchange rate has been quoted

        Type: str
        """
        return self.__quotation_date_time

    @quotation_date_time.setter
    def quotation_date_time(self, value: str):
        self.__quotation_date_time = value

    @property
    def source(self) -> str:
        """
        | Indicates the exchange rate source name. The rate source is supplied for receipt printing purposes and to meet regulatory requirements where applicable

        Type: str
        """
        return self.__source

    @source.setter
    def source(self, value: str):
        self.__source = value

    def to_dictionary(self):
        dictionary = super(RateDetails, self).to_dictionary()
        if self.exchange_rate is not None:
            dictionary['exchangeRate'] = self.exchange_rate
        if self.inverted_exchange_rate is not None:
            dictionary['invertedExchangeRate'] = self.inverted_exchange_rate
        if self.mark_up_rate is not None:
            dictionary['markUpRate'] = self.mark_up_rate
        if self.quotation_date_time is not None:
            dictionary['quotationDateTime'] = self.quotation_date_time
        if self.source is not None:
            dictionary['source'] = self.source
        return dictionary

    def from_dictionary(self, dictionary):
        super(RateDetails, self).from_dictionary(dictionary)
        if 'exchangeRate' in dictionary:
            self.exchange_rate = dictionary['exchangeRate']
        if 'invertedExchangeRate' in dictionary:
            self.inverted_exchange_rate = dictionary['invertedExchangeRate']
        if 'markUpRate' in dictionary:
            self.mark_up_rate = dictionary['markUpRate']
        if 'quotationDateTime' in dictionary:
            self.quotation_date_time = dictionary['quotationDateTime']
        if 'source' in dictionary:
            self.source = dictionary['source']
        return self
