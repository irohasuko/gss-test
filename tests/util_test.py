import util

def test_remove_blank():
    arg_data = ['a', 'b ', 'c  ']
    expected = ['a', 'b', 'c']
    assert util.remove_blank(arg_data) == expected

def test_extract_file_name(mocker):
    mocker.patch("os.listdir", return_value=['first.csv', 'second.csv', 'third.csv'])
    expected = ['second.csv', 'third.csv']
    assert util.extract_file_name() == expected

def test_extract_unv_data():
    arg_data = {
        ('10', 'aaa', 'bb'),
        ('70', 'aaa', 'bb'),
        ('8000', 'aaa', 'bb')
    }
    
    expected = {
        ('10', 'aaa', 'bb'),
        ('70', 'aaa', 'bb')
    }
    
    assert util.extract_unv_data(arg_data) == expected

def test_extract_dif_by_compare_cd():
    base = {
        ('11', '12', '13', '14', '15', '16', '1000'),
        ('21', '22', '23', '24', '25', '26', '2000'),
        ('31', '32', '33', '34', '35', '36', '3000'),
    }
    
    compare = {
        ('11', '12', '13', '14', '15', '16', '1000'),
        ('21', '22', '23', '24', '25', '26', '2001'),
        ('31', '32', '33', '34', '35', '36', '3000'),
    }
    
    expected = {
        ('21', '22', '23', '24', '25', '26', '2000')
    }
    
    assert util.extract_dif_by_compare_cd(base, compare) == expected