from datetime import date, datetime
from typing import Tuple
import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from kes.proto.table_pb2 import AddRowsRequest, ImageValue, LocationPoint, LocationValues, ReadTableRequest, Row, Rows, SaveImageReply, SaveImageRequest

from tables import CategoryAssetRow, Multipleselect, Singleselect, category_asset_table_def
from kes.table import Table


class TestRow(unittest.TestCase):
    def test_isolation(self):
        # should run against generated rows.

        row1 = CategoryAssetRow()
        row2 = CategoryAssetRow()

        self.assertIsNot(row1.location, row2.location)
        self.assertIsNot(row1.image, row2.image)


@patch('kes.table.uuid4')
class TestTable(unittest.TestCase):
    def setUp(self):
        self.tableStub = Mock()
        self.tableUuid = uuid4()
        self.activityUuid = uuid4()
        self.rowId = uuid4()
        self.table = Table[CategoryAssetRow](
            self.tableStub, self.activityUuid, CategoryAssetRow, self.tableUuid, category_asset_table_def.property_map
        )
        self.row = CategoryAssetRow(
            singleselect=Singleselect.A,
            multipleselect=Multipleselect.F | Multipleselect.D,
            amount=3.0,
            text="Text",
            dateproperty=datetime.combine(date.today(), datetime.min.time())
        )

    def test_append_row_primitive_fields(self, mock_uuid: Mock):
        mock_uuid.return_value = self.rowId
        ref = self.table.append_row(self.row)

        req, row = self._build_rows_request()
        field_singleselect = row.fields.add()
        field_singleselect.propertyId = 'd0165c6c-3a53-4126-b701-44cab335853a'
        field_singleselect.members.elements.append(3)
        field_text = row.fields.add()
        field_text.propertyId = 'da1df664-e1ae-4b00-aef5-8e5d86ec74da'
        field_text.strings.elements.append("Text")
        field_number = row.fields.add()
        field_number.propertyId = 'f03d4f5f-a76c-4f20-ab89-5e452b437627'
        field_number.numbers.elements.append(3.0)
        field_multiselect = row.fields.add()
        field_multiselect.propertyId = '7cfdbda8-02e3-47b5-9dae-aa8246baf5d3'
        field_multiselect.members.elements.append(1)
        field_multiselect.members.elements.append(3)
        field_date = row.fields.add()
        field_date.propertyId = '828f345c-0e02-49ff-8766-41cabc38dcee'
        field_date.date.FromDatetime(datetime.combine(date.today(), datetime.min.time()))
        self.tableStub.addRows.assert_called_once_with(req)    # type: ignore

        self.assertEqual(ref.asset_type_id, self.tableUuid)

    def test_append_row_image(self, mock_uuid: Mock):
        mock_uuid.return_value = self.rowId
        self.tableStub.saveImage.return_value = SaveImageReply(tempKey="tempKey")  # type: ignore

        image_row = CategoryAssetRow()
        fake_image = "FAKE_IMAGE"
        self.table.save_image(image_row.image, "image_name", fake_image.encode())
        self.table.append_row(image_row)

        req, row = self._build_rows_request()
        field_image = row.fields.add()
        field_image.propertyId = "10f11f64-cdce-4ca7-9266-8afeb3a87f6c"
        field_image.image.fileName = "image_name"
        field_image.image.tempKey = "tempKey"

        self.tableStub.addRows.assert_called_once_with(req)  # type: ignore
        self.tableStub.saveImage.assert_called_once()  # type: ignore

    def test_append_location(self, mock_uuid: Mock):
        mock_uuid.return_value = self.rowId

        location_row = CategoryAssetRow()
        location_row.location.add_point("point", 3.3, 6.6, "address")
        self.table.append_row(location_row)

        req, row = self._build_rows_request()
        field_location = row.fields.add()
        field_location.propertyId = "39a81418-d542-46d5-959b-924a51c4885b"

        point = LocationPoint(name = "point", latitude=3.3, longitude=6.6, address="address")
        field_location.locations.elements.append(point)

        self.tableStub.addRows.assert_called_once_with(req)  # type: ignore

    def _build_rows_request(self) -> Tuple[AddRowsRequest, Row]:
        req = AddRowsRequest()
        row = req.rows.add()
        row.assetId = str(self.rowId)
        req.activityId = str(self.activityUuid)
        req.tableId = str(self.tableUuid)
        return req, row  # type: ignore

    def test_append_empty_row(self, mock_uuid: Mock):
        mock_uuid.return_value = self.rowId
        emptyRow = CategoryAssetRow()
        self.table.append_row(emptyRow)

        req, _ = self._build_rows_request()

        self.tableStub.addRows.assert_called_once_with(req)    # type: ignore

    def test_append_integer(self, mock_uuid: Mock):
        mock_uuid.return_value = self.rowId
        rowWithInteger = CategoryAssetRow(amount=3)
        self.table.append_row(rowWithInteger)

        req, row = self._build_rows_request()
        field_number = row.fields.add()
        field_number.propertyId = 'f03d4f5f-a76c-4f20-ab89-5e452b437627'
        field_number.numbers.elements.append(3.0)

        self.tableStub.addRows.assert_called_once_with(req)    # type: ignore

    def test_load_row(self, _):
        response = Rows()
        row = response.rows.add()
        row.assetId = str(self.rowId)
        field_number = row.fields.add()
        field_number.propertyId = 'f03d4f5f-a76c-4f20-ab89-5e452b437627'
        field_number.multi = False
        field_number.numbers.elements.append(3.0)
        field_text = row.fields.add()
        field_text.propertyId = 'da1df664-e1ae-4b00-aef5-8e5d86ec74da'
        field_text.multi = False
        field_text.strings.elements.append('Text')
        field_single_select = row.fields.add()
        field_single_select.propertyId = 'd0165c6c-3a53-4126-b701-44cab335853a'
        field_single_select.multi = False
        field_single_select.members.elements.append(3)
        field_multi_select = row.fields.add()
        field_multi_select.propertyId = '7cfdbda8-02e3-47b5-9dae-aa8246baf5d3'
        field_multi_select.multi = False
        field_multi_select.members.elements.append(1)
        field_multi_select.members.elements.append(3)
        field_date = row.fields.add()
        field_date.propertyId = '828f345c-0e02-49ff-8766-41cabc38dcee'
        field_date.multi = False
        field_date.date.FromDatetime(datetime.combine(date.today(), datetime.min.time()))
        mockLoad = Mock(return_value=response)
        self.tableStub.attach_mock(mockLoad, 'readTable')
        self.table.load()

        req = ReadTableRequest()
        req.activityId = str(self.activityUuid)
        req.tableId = str(self.tableUuid)
        mockLoad.assert_called_once_with(req)

        self.assertSequenceEqual(self.table, [self.row])

    def test_iteration(self, _):
        row1 = CategoryAssetRow(text="Roel de Jong")
        row2 = CategoryAssetRow(text="John Carmack")
        self.table.append_row(row1)
        self.table.append_row(row2)

        programmer_iter = iter(self.table)
        programmer = next(programmer_iter)
        self.assertEqual(programmer.text, "Roel de Jong")
        programmer = next(programmer_iter)
        self.assertEqual(programmer.text, "John Carmack")
        with self.assertRaises(StopIteration):
            next(programmer_iter)

    def test_reverse_iteration(self, _):
        row1 = CategoryAssetRow(text="Roel de Jong")
        row2 = CategoryAssetRow(text="John Carmack")
        self.table.append_row(row1)
        self.table.append_row(row2)

        programmer_iter = reversed(self.table)
        programmer = next(programmer_iter)
        self.assertIs(programmer.text, "John Carmack")
        programmer = next(programmer_iter)
        self.assertEqual(programmer.text, "Roel de Jong")
        with self.assertRaises(StopIteration):
            next(programmer_iter)

    def test_len(self, _):
        self.assertEqual(len(self.table), 0)

        programmer = CategoryAssetRow()
        self.table.append_row(programmer)
        self.assertEqual(len(self.table), 1)


if __name__ == '__main__':
    unittest.main()
