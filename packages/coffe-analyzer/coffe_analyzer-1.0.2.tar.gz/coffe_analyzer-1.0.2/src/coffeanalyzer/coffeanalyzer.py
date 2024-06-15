import pandas
from sympy.logic.boolalg import to_dnf, to_cnf, simplify_logic


class CoffeInstance:
    """
    A class that represents a CoFFE analysis.

    CoFFE stands for Combinational Functional Failures Effects. One method of 
    performing this analysis is through a table. Each row of that table represents
    a combination of failures leading to a certain result. The CoFFE analysis helps 
    to develop the preliminary FTA and failure conditions which may be allocated 
    to systems/equipment.
    
    Attributes
    ----------
    ignored_states : list, optional
        The states that shall be ignored as failures. The value by default is [].
    ignored_results : list, optional
        The results of the combination of failures not relevant for the analysis. 
        The value by default is [].
    custom_headers : list, optional
        Variable names for the boolean expression, if not defined A, B, ... are used. 
        The value by default is [].
    
    Methods
    -------
    get_simplified_expression_from_csv(csv_path, csv_delimiter = ';')
        Reduces each of the results of the CoFFE table (from a csv) to the 
        most simplified boolean expression leading to that result.

    Examples
    -------
    get_simplified_expression_from_csv example

    >>> path_csv = 'path/to/csv/file.csv'
    >>> coffe_csv = CoffeInstance(ignored_states=['O'], ignored_results=['Partial Loss', 'No Loss'])
    >>> coffe_results = coffe_csv.get_simplified_expression_from_csv(path_csv)
    >>> print(coffe_results)
    {'Total Loss': '(A_F AND B_F) OR (C_F AND D_F)'}
    """

    def __init__(
            self, 
            ignored_states: list[str] = [], 
            ignored_results: list[str] = [], 
            custom_headers: list[str] = []
            ) -> None:
        """
        Parameters
        ----------
        ignored_states : list[str], optional
            The states that shall be ignored as failures. The value by default is [].
        ignored_results : list[str], optional
            The results of the combination of failures not relevant for the analysis.
            The value by default is [].
        custom_headers : list[str] optional
            Variable names for the boolean expression, if not defined A, B, ... are used.
            The value by default is [].
        """

        self.ignored_states = ignored_states
        self.ignored_results = ignored_results
        self.custom_headers = custom_headers
        
        if self.custom_headers == []:
            self._default_headers = [chr(letter) for letter in range(65, 91)]
            self.apply_custom_headers = False
        else:
            self.apply_custom_headers = True

        self.coffe_summary = {}

        self.or_gate = ' | '
        self.and_gate = ' & '
        self.start_row = '('
        self.end_row = ')'
    
    @property
    def ignored_states(self) -> list[str]:
        return self._ignored_states
    
    @ignored_states.setter
    def ignored_states(self, ignored_states: list[str]):
        self._ignored_states = ignored_states

    @property
    def ignored_results(self) -> list[str]:
        return self._ignored_results
    
    @ignored_results.setter
    def ignored_results(self, ignored_results: list[str]) -> None:
        self._ignored_results = ignored_results

    @property
    def custom_headers(self) -> list[str]:
        return self._custom_headers
    
    @custom_headers.setter
    def custom_headers(self, custom_headers: list) -> None:
        self._custom_headers = custom_headers

    def get_simplified_expression_from_csv(self, csv_path:str, csv_delimiter:str = ';') -> dict[str, str]:
        """Reduces each of the results of the CoFFE table (from a csv) to the 
        most simplified boolean expression leading to that result.

        From a csv file a pandas' DataFrame is generated and is info is extracted.
        A general expression is obtained as the sum of each row related to a 
        certain result (Failure Condition). That expression is reduced to its
        simplest form to support the generation of the relevant Fault Tree 
        Analysis (FTA).

        Parameters
        ----------
        csv_path : str
            The file path of the csv file containing the CoFFE analysis table.
        csv_delimiter : str, optional
            Character that separate values in the csv file. Delimiters frequently used 
            include the comma, tab, space, and semicolon. The value by default is ';'.

        Returns
        -------
        dict[str, str]
            A dictionary where each key is a CoFFE result (Failure Condition) and their 
            value is the simplified boolean expression.

        Examples
        -------
        >>> path_csv = 'path/to/csv/file.csv'
        >>> coffe_csv = CoffeInstance(ignored_states=['O'], ignored_results=['Partial Loss', 'No Loss'])
        >>> coffe_results = coffe_csv.get_simplified_expression_from_csv(path_csv)
        >>> print(coffe_results)
        {'Total Loss': '(A_F AND B_F) OR (C_F AND D_F)'}
        """

        df = self.__get_dataframe_from_csv(csv_path, csv_delimiter)
        self.__get_info_from_dataframe(df)
        result_dict = self.__get_result_dict()
        return result_dict
    
    def __get_dataframe_from_csv(self, csv_path: str, csv_delimiter: str) -> pandas.DataFrame:
        """From a csv file a pandas' DataFrame is generated.

        Parameters
        ----------
        csv_path : str
            The file path of the csv file containing the CoFFE analysis table.
        csv_delimiter : str
            Character that separate values in the csv file. Delimiters frequently used 
            include the comma, tab, space, and semicolon. The inherited value by default 
            is ';'.
        
        Returns
        -------
        pandas.DataFrame
            Structure that contains two-dimensional data that represents the CoFFE table.
        """

        return pandas.read_csv(csv_path, delimiter = csv_delimiter)

    def __get_info_from_dataframe(self, df: pandas.DataFrame) -> None:
        """Sets a dictionary to store relevant CoFFE results as boolean expressions,
        obtains them and stored back to the dictionary.

        Parameters
        ----------
        df : pandas.DataFrame
            Structure that contains two-dimensional data that represents the CoFFE table.
        """

        self.__set_coffe_summary_dict(df)
        self.__get_boolean_expressions(df)

    def __set_coffe_summary_dict(self, df: pandas.DataFrame) -> None:
        """Calulates the list of results contained in the CoFFE table, filters 
        which are relevant for the analysis and sets a dictionary to store their 
        boolean expressions.

        The dict has the following form: 
            self.coffe_summary[key] = {
                'expr': '',
                'simplified_expr': ''
                }

        Parameters
        ----------
        df : pandas.DataFrame
            Structure that contains two-dimensional data that represents the CoFFE table.
        """

        results = df.iloc[:, -1].unique().tolist()
        for result in results:
            if result not in self.ignored_results:
                self.coffe_summary[result] = {'expr': '', 'simplified_expr': ''}

    def __get_boolean_expressions(self, df: pandas.DataFrame) -> None:
        """The general boolean expression is obtained for each relevant CoFFE 
        result (Failure Condition). Then it is simplified and both are stored in 
        self.coffe_summary_dict.

        The general boolean expression is obtained as a sum of each row related to
        the CoFFE result under consideration. 

        Parameters
        ----------
        df : pandas.DataFrame
            Structure that contains two-dimensional data that represents the CoFFE table.

        Raises
        ------
        ValueError
            If the custom_headers attribute is incoherent with the size of the DataFrame.
        """

        num_columns = len(df.columns)
        results_column = num_columns - 1

        if self.apply_custom_headers:
            if len(self.custom_headers) == num_columns - 1:
                headers = self.custom_headers
            else:
                error_msg = "The length of thedefined headers is not of the same size than the data."
                raise ValueError(error_msg)
        else:
            headers = self._default_headers
        
        for _, row in df.iterrows():
            result = row.iloc[results_column]
            if result not in self.ignored_results:
                row_expression = ''
                for i in range(num_columns - 1):
                    state = row.iloc[i].replace(" ", "")
                    if state not in self.ignored_states:
                        if row_expression == '':
                            row_expression = ''.join([self.start_row, f'{headers[i]}_{state}'])
                        else:
                            row_expression = ''.join([row_expression, self.and_gate, f'{headers[i]}_{state}'])
                row_expression = ''.join([row_expression, self.end_row, self.or_gate])
                self.coffe_summary[result]['expr'] = ''.join([self.coffe_summary[result]['expr'], row_expression])
        
        for key in self.coffe_summary:
            self.coffe_summary[key]['expr'] = self.coffe_summary[key]['expr'][:-3]
            self.coffe_summary[key]['simplified_expr'] = self.__simplify_boolean_expression(self.coffe_summary[key]['expr'])

    def __simplify_boolean_expression(self, expr):
        """Simplifies a boolean expression.

        This function evaluates three different methods from Sympy (sympy.logic.boolalg -
        to_dnf, to_cnf, and simplify), and gets the reduction that has the minimum length
        (the simplest one). 

        Parameters
        ----------
        expr : str
            General boolean expression obtained from the CoFFE table for a certain
            result (Failure Condition).

        Returns
        -------
        str
            Simplified boolean expression obtained from the general one.
        """

        expr_list = [
            str(to_dnf(expr, simplify=True, force=True)),
            str(simplify_logic(expr, force=True)),
            str(to_cnf(expr, simplify=True, force=True))
            ]
        
        expr_len = [len(boolean_expr) for boolean_expr in expr_list]
        min_expr_index = expr_len.index(min(expr_len))

        return expr_list[min_expr_index]
            
    def __get_result_dict(self) -> dict[str, str]:
        """Simplifies the complete dictionary with the complete CoFFE analysis data to
        another dictionary to show the results.

        Returns
        -------
        dict[str, str]
            A dictionary where each key is a CoFFE result (Failure Condition) and their 
            value is the simplified boolean expression.
        """

        result_dict = {}
        for key in self.coffe_summary:
            result_dict[key] = str(
                self.coffe_summary[key]['simplified_expr']
                ).replace(self.and_gate, " AND ").replace(self.or_gate, " OR ")

        return result_dict
