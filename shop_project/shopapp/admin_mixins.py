import csv
from django.db.models.options import Options
from django.http import HttpResponse


class ExportAsCSVMixin:
    def export_as_csv(self, request, queryset):
        meta: Options = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv;charset=windows-1251")
        response["Content-Disposition"] = "attachment; filename={}-export.csv".format(
            meta
        )
        result = csv.writer(
            response,
            dialect="excel-tab",
            quoting=csv.QUOTE_NONNUMERIC
        )
        result.writerow(field_names)
        for obj in queryset:
            result.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export as CSV"
