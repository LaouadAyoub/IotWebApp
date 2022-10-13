from FactoryData import FactoryData
process_names = [
    'cycle_time',
    'time_to_complete',
    'safety_materials',
    'safety_manufacturing',
    'safety_packing',
    'panne1',
    'manufacturing_temp',
    'manufacturing_humi',
    'production_levels',

]
fdata = FactoryData(process_names)

stats = [fdata.get_data()[pname] for pname in process_names]

print(stats)