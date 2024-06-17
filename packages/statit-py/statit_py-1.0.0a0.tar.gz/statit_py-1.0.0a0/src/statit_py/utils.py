from typing import Callable

def table_to_obs(table: list[list], line_to_date: Callable[[list], str | None], line_to_value: Callable[[list], int | float | None], line_to_key: Callable[[list], str | None]) -> dict[str, list[tuple[str, int | float | None]]]:
     """
     Takes a table (CSV file) and outputs a dictionary of observations

     Arguments
     ----------
          table : list(list)
               A list of lines (such as in a CSV file)
          line_to_date : (list) -> str | None
               A function whose input is a line and output is the corresponding date, if there exists one
          line_to_value : (list) -> int | float | None
               A function whose input is a line and output is the corresponding value, if there exists one
          line_to_key : (list) -> str | None
               A function whose input is a line and output is the corresponding key of the serie, if there exists one

     Out
     ---
     A dictionary whose values are a list of observations

     """
     #create observation lists, mapped by id
     key_datified = {
        (line_to_key(line),line_to_date(line),str(i)) : line_to_value(line)
        for line,i in zip(table,range(len(table)))
        if line_to_date(line) and line_to_key(line)
     }
     aggregated = {}
     for key, value in key_datified.items():
            k = (key[0], key[1])
            try:
               if not k in aggregated:
                    aggregated[k] = value if (value!=None and value!='') else 0
               else:
                    aggregated[k] += value              
            except(TypeError):
                pass

     observations = {}
     for key, value in aggregated.items():
          if not key[0] in observations:
               observations[key[0]] = [(key[1], value)]
          else:
               observations[key[0]].append((key[1], value))

     return observations

