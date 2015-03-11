from items import Item

class Table():

    def __init__(self,
                 table_path,
                 header_path='path',
                 header_extractor='path',
                 row_path='path',
                 column_path='path',
                 column_extractor='path',
                 item=Item):

        self.table_path       = table_path
        self.header_path      = header_path
        self.header_extractor = header_extractor
        self.row_path         = row_path
        self.column_path      = column_path
        self.column_extractor = column_extractor
        self.item = item

    def items(self, sel):
        table = sel.xpath(self.table_path)
        header_row = table.xpath(self.header_path)
        headers = header_row.xpath(self.header_extractor).extract()
        rows = table.xpath(self.row_path)
        for row in rows:
            item = self.item()
            columns = row.xpath(self.column_extractor).extract()
            for h, c in zip(headers, columns):
                item[h] = c
            yield item
