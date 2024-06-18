class OrderMsg:
    def __init__(self):
        self.oid = ''
        self.sid = ''
        self.mudan_id = ''
        self.order_dict = {}
        self.traded_vol = 0
        self.traded_amt = 0.0
        self.local_ids = []

    def set_oid(self, oid):
        self.oid = oid

    def get_oid(self):
        return self.oid

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid

    def set_mudan_id(self, mudan_id):
        self.mudan_id = mudan_id

    def get_mudan_id(self):
        return self.mudan_id

    def set_order_dict(self, order_dict):
        self.order_dict = order_dict

    def get_order_dict(self):
        return self.order_dict

    def set_traded_vol(self, traded_vol):
        self.traded_vol = traded_vol

    def get_traded_vol(self):
        return self.traded_vol

    def set_traded_amt(self, traded_amt):
        self.traded_amt = traded_amt

    def get_traded_amt(self):
        return self.traded_amt

    def set_local_ids(self, local_ids):
        self.local_ids = local_ids

    def get_local_ids(self):
        return self.local_ids
