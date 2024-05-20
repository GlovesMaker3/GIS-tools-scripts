# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Obliczenie"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Obliczanie populacji i powierzchni by Daniel"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Warstwa z powierzchnią i maska jednocześnie",
            name="plik_wejsciowy",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Raster",
            name="Raster",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Populacja (punkty)",
            name="Populacja (punkty)",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param3 = arcpy.Parameter(
            displayName="Populacja pole z tabeli odpowiedzające za populacje",
            name="Populacja pole z tabeli odpowiedzające za populacje",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        param4 = arcpy.Parameter(
            displayName="Populacja pole z tabeli odpowiedzające za populacje (opcjonalnie 1)",
            name="Populacja pole z tabeli odpowiedzające za populacje (opcjonalnie 1)",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        param5 = arcpy.Parameter(
            displayName="Populacja pole z tabeli odpowiedzające za populacje (opcjonalnie 2)",
            name="Populacja pole z tabeli odpowiedzające za populacje (opcjonalnie 2)",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        param6 = arcpy.Parameter(
            displayName="Wynik",
            name="Wynik",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")


        params = [param0, param1, param2, param3, param4, param5, param6]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Aktualizacja parametrów"""

        if parameters[2].value:  # Sprawdź czy parametr 2 ma wartość
            columns = arcpy.ListFields(parameters[2].value)  # Pobierz listę kolumn
            column_names = [column.name for column in columns]  # Pobierz nazwy kolumn
            # Przypisz listę nazw kolumn do parametru param3
            parameters[3].filter.list = column_names

            parameters[4].filter.list = column_names
            parameters[5].filter.list = column_names
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        def get_summarized_value(summarize_layer, field_name):
            summarized_value = None
            with arcpy.da.SearchCursor(summarize_layer, [f"SUM_{field_name}"]) as cursor:
                for row in cursor:
                    summarized_value = row[0]
                    break  # Assuming there's only one row, we can break after the first iteration

            return summarized_value

        def update_summarized_value(feature_class, field_name, summarized_value):
            with arcpy.da.UpdateCursor(feature_class, [field_name]) as cursor:
                for row in cursor:
                    row[0] = summarized_value
                    cursor.updateRow(row)




        plik_wejsciowy = parameters[0].valueAsText
        Raster_warstwa = parameters[1].valueAsText
        Populacja_warstwa = parameters[2].valueAsText

        Populacja_pole_w_warstwie = parameters[3].valueAsText
        Populacja_pole_w_warstwie_2 = parameters[4].valueAsText
        Populacja_pole_w_warstwie_3 = parameters[5].valueAsText

        arcpy.management.AddField(plik_wejsciowy, "Powierzchnia_dla_AOI", "DOUBLE")
        #arcpy.management.AddField(plik_wejsciowy, "Populacja_dla_AOI", "DOUBLE")

        arcpy.management.CalculateGeometryAttributes(
            plik_wejsciowy,
            [["Powierzchnia_dla_AOI", "AREA_GEODESIC"]],
            area_unit="SQUARE_METERS"
        )

################################################### PARAMETR NR 0####################################################################
        if parameters[3].value:
            arcpy.management.AddField(plik_wejsciowy, "Populacja_dla_AOI", "DOUBLE")
            SummarizeWithin_layer_1 = arcpy.analysis.SummarizeWithin(
                plik_wejsciowy,
                Populacja_warstwa,
                "in_memory/SummarizeWithin_layer_1",
                "KEEP_ALL",
                [[Populacja_pole_w_warstwie, "SUM"]]
            )

            summarized_value_1 = get_summarized_value(SummarizeWithin_layer_1, Populacja_pole_w_warstwie)

            if summarized_value_1 is not None:
                update_summarized_value(plik_wejsciowy, "Populacja_dla_AOI", summarized_value_1)


################################################### PARAMETR OPCJONALNY NR 1####################################################################
        if parameters[4].value:
            arcpy.management.AddField(plik_wejsciowy, "Populacja_dla_AOI_opcjonalnie_1", "DOUBLE")
            SummarizeWithin_layer_2 = arcpy.analysis.SummarizeWithin(
                plik_wejsciowy,
                Populacja_warstwa,
                "in_memory/SummarizeWithin_layer_2",
                "KEEP_ALL",
                [[Populacja_pole_w_warstwie_2, "SUM"]]
            )
            summarized_value_2 = get_summarized_value(SummarizeWithin_layer_2, Populacja_pole_w_warstwie_2)

            if summarized_value_2 is not None:
                update_summarized_value(plik_wejsciowy, "Populacja_dla_AOI_opcjonalnie_1", summarized_value_2)


################################################### PARAMETR OPCJONALNY NR 2####################################################################
        if parameters[5].value:
            arcpy.management.AddField(plik_wejsciowy, "Populacja_dla_AOI_opcjonalnie_2", "DOUBLE")
            SummarizeWithin_layer_3 = arcpy.analysis.SummarizeWithin(
                plik_wejsciowy,
                Populacja_warstwa,
                "in_memory/SummarizeWithin_layer_3",
                "KEEP_ALL",
                [[Populacja_pole_w_warstwie_3, "SUM"]]
            )
            summarized_value_3 = get_summarized_value(SummarizeWithin_layer_3, Populacja_pole_w_warstwie_3)
            if summarized_value_3 is not None:
                update_summarized_value(plik_wejsciowy, "Populacja_dla_AOI_opcjonalnie_2", summarized_value_3)






################################################### ExtractByMask ####################################################################
        out_raster = arcpy.sa.ExtractByMask(Raster_warstwa, plik_wejsciowy, "INSIDE")

        arcpy.AddMessage(f'Raster wejściowy dla ExtractByMask: {Raster_warstwa}')
        arcpy.AddMessage(f'Maska dla ExtractByMask: {plik_wejsciowy}')

        RasterToPolygon_layer_4 = arcpy.conversion.RasterToPolygon(out_raster, "in_memory/RasterToPolygon_layer_4")


 ################################################### Zapisanie wyniku ####################################################################
        Wynik_6 = parameters[6].valueAsText

        arcpy.management.Dissolve(RasterToPolygon_layer_4, Wynik_6, dissolve_field=["gridcode"])




        arcpy.management.AddField(Wynik_6, "Calkowita_populacja", "DOUBLE")
        arcpy.management.AddField(Wynik_6, "Calkowita_populacja_opcjonalna_1", "DOUBLE")
        arcpy.management.AddField(Wynik_6, "Calkowita_populacja_opcjonalna_2", "DOUBLE")






        fields_to_update = ["Calkowita_powierzchnia_indoor_outdoor"]
        fields_to_search = ["Powierzchnia_dla_AOI", "Populacja_dla_AOI"]


        if parameters[3].value:
            arcpy.management.AddField(Wynik_6, "Statystyka_populacja", "DOUBLE")


            fields_to_search.append("Populacja_dla_AOI")
            fields_to_update.append("Calkowita_populacja")
        else:
            arcpy.management.DeleteField(Wynik_6, "Calkowita_populacja")



        if parameters[4].value:
            fields_to_search.append("Populacja_dla_AOI_opcjonalnie_1")
            fields_to_update.append("Calkowita_populacja_opcjonalna_1")
        else:
            arcpy.management.DeleteField(Wynik_6, "Calkowita_populacja_opcjonalna_1")




        if parameters[5].value:
            fields_to_search.append("Populacja_dla_AOI_opcjonalnie_2")
            fields_to_update.append("Calkowita_populacja_opcjonalna_2")
        else:
            arcpy.management.DeleteField(Wynik_6, "Calkowita_populacja_opcjonalna_2")







        with arcpy.da.SearchCursor(plik_wejsciowy, fields_to_search) as cursor:
            for row in cursor:
                powierzchnia_value = row[0]

                if parameters[3].value:
                    populacja_value = row[1]
                if parameters[4].value:
                    populacja_value_1 = row[2]
                if parameters[5].value:
                    populacja_value_2 = row[3]
                break  # Ponieważ mamy tylko jeden rekord, przerywamy pętlę po jego odczytaniu

        # Ścieżka do warstwy wynikowej, do której chcemy przypisać wartości


        # Aktualizujemy pola w warstwie Wynik_6
        with arcpy.da.UpdateCursor(Wynik_6, fields_to_update) as cursor:
            for row in cursor:
                row[0] = powierzchnia_value  # Przypisujemy stałą wartość Powierzchnia_dla_AOI
                arcpy.AddMessage(f'Powierzchnia całkowita: {powierzchnia_value} [mkw]')
                if parameters[3].value:
                    row[1] = populacja_value    # Przypisujemy stałą wartość Populacja_dla_AOI
                    arcpy.AddMessage(f'Household : {populacja_value}')
                if parameters[4].value:
                    row[2] = populacja_value_1
                if parameters[5].value:
                    row[3] = populacja_value_2

                cursor.updateRow(row)




        arcpy.management.AddField(Wynik_6, "Statystyka_powierzchnia_indoor_outdoor", "DOUBLE")
        #arcpy.management.AddField(Wynik_6, "Statystyka_populacja", "DOUBLE")




        # pola, które na pewno są
        fields_to_update_statystyka = ["Statystyka_powierzchnia_indoor_outdoor","Calkowita_powierzchnia_indoor_outdoor", "Shape_Area"]





        # Przechowujemy wartości z pierwszego i drugiego przejścia
        wartosci = []

        with arcpy.da.UpdateCursor(Wynik_6, fields_to_update_statystyka) as cursor:
            for row in cursor:
                # Obliczamy wartość dla bieżącego wiersza
                row[0] = (row[2]/row[1])*100
                # Zapisujemy wartość do listy
                wartosci.append(row[0])
                # Zapisujemy zmiany w bieżącym wierszu
                cursor.updateRow(row)

        # Wymuszamy "trzecie przejście" ręcznie, aktualizując pierwszy wiersz
        with arcpy.da.UpdateCursor(Wynik_6, fields_to_update_statystyka) as cursor:
            for i, row in enumerate(cursor):
                if i == 0:  # Dla pierwszego wiersza
                    # Sumujemy wartości z obu wierszy i zapisujemy w pierwszym wierszu
                    row[0] += wartosci[1]
                    cursor.updateRow(row)
                    break  # Kończymy pętlę po zaktualizowaniu pierwszego wiersza

        # ZRÓB TO KURSOREM
        #arcpy.management.CalculateField(plik_wejsciowy, field="Statystyka_powierzchnia_indoor_outdoor", expression=f"({powierzchnia_indoor_outdoor}/!Powierzchnia_dla_AOI!)*100", expression_type="PYTHON3")


        return



    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
