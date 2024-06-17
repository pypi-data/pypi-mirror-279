class PandasMock:
    class DataFrame:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "pandas is required for this method. Please install it using `pip install pandas`. "
                "For more information, check the variable from crimson.data_class import requirements"
            )


pd = PandasMock()

try:
    import pandas as pd
except ImportError:
    pass
