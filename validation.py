class DataValidator:
    def validate(
        self,
        value,
        check_on_empty_line=None,
        check_on_dash=None,
        check_on_two_parts=None,
        check_on_two_parts_with_dash=None,
        check_on_length=None,
        check_on_two_values=None,
        check_on_range_with_dash=None,
        check_on_range=None
    ):
        
        if check_on_empty_line:
            self._check_empty_line(value)
        
        if check_on_dash:
            self._check_dash(value)
        
        if check_on_two_parts:
            self._check_two_parts(value)
        
        if check_on_two_parts_with_dash:
            self._check_two_parts_with_dash(value)
        
        if check_on_length:
            self._check_length(value, check_on_length)
        
        if check_on_two_values:
            self._check_two_values(value)
        
        if check_on_range_with_dash:
            self._check_range_with_dash(value, check_on_range_with_dash)
        
        if check_on_range:
            self._check_range(value, check_on_range)
    
    def _check_empty_line(self, value):
        """Проверка на пустую строку."""
        if not value:
            raise ValueError('Пустая строка')
    
    def _check_dash(self, value):
        """Проверка наличия дефиса."""
        if '-' not in value:
            raise ValueError('Нет тире')
    
    def _check_two_parts(self, value):
        """Проверка на две части."""
        if not len(value) == 2:
            raise ValueError(
                'Неверное количество частей. '
                'Должно быть 2 части, разделенные тире.'
            )
    
    def _check_two_parts_with_dash(self, value):
        """Проверка на две части с разделителем дефис."""
        if len(value.split('-')) != 2:
            raise ValueError('Ошибка с тире')
    
    def _check_length(self, value, max_length):
        """Проверка максимальной длины строки."""
        if len(value) > max_length:
            raise ValueError('Строка слишком длинная')
    
    def _check_two_values(self, value):
        """Проверка двух числовых значений, разделенных дефисом."""
        if '-' not in value:
            raise ValueError('Нет тире')
        
        part1, part2 = value.split('-')
        part1 = float(part1)
        part2 = float(part2)
        
        if part1 > part2:
            raise ValueError('Первое значение больше второго')
    
    def _check_range_with_dash(self, value, valid_range):
        """Проверка двух значений в диапазоне, разделенных дефисом."""
        if '-' not in value:
            raise ValueError('Нет тире')
        
        part1, part2 = value.split('-')
        part1 = float(part1)
        part2 = float(part2)
        
        min_val, max_val = valid_range
        if not (min_val <= part1 <= max_val) or not (min_val <= part2 <= max_val):
            raise ValueError(
                f'Значение должно быть в диапазоне от {min_val} до {max_val}'
            )
    
    def _check_range(self, value, valid_range):
        """Проверка одиночного значения в диапазоне."""
        min_val, max_val = valid_range
        if not min_val <= float(value) <= max_val:
            raise ValueError(
                f'Значение должно быть в диапазоне от {min_val} до {max_val}'
            )