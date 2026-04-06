import pytest
import os


@pytest.fixture
def instructions_from_filename(request: pytest.FixtureRequest) -> str:
    """Reads file based on filename found in **tests/fixtures**

    Args:
        request (pytest.FixtureRequest): Name of the file to be read

    Returns:
        list[str]: List of stripped lines
    """
    filename = request.param
    file_path = os.path.join("tests", "fixtures", filename)
    with open(file_path, "r") as f:
        return f.read()


@pytest.fixture
def no_bottom():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T|
 1   2   3   4

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def multiple_bottom():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T|
 1   2   3   4
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
bottom
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def no_stack_numbers():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T|
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def no_boxes():
    return """
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def empty_boxes():
    return """
|K|            
|A| | |     |F|
|P| |U| |B| ||
 1   2   3   4
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def more_than_max_stacks():
    return """
|K|             |L|                        
|A| |Q|     |F| |Y| |M|     |I| |X|     |J|
|P| |U| |B| |T| |W| |R| |O| |Z| |G| |N| |E|
 1   2   3   4   5   6   7   8   9   10  11
                    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def invalid_movements():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T|
 1   2   3   4
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
mov 1 from 1 to 2
move 2 from 4 to 1
"""


@pytest.fixture
def no_movements():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T|
 1   2   3   4
    bottom

"""

@pytest.fixture
def more_stacks_than_ids():
    return """
|K|            
|A| |Q|     |F|
|P| |U| |B| |T| |X|
 1   2   3   4     
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""

@pytest.fixture
def more_ids_than_stacks():
    return """
|K|            
|A| |Q|        
|P| |U| |B|    
 1   2   3   4
    bottom

move 1 from 3 to 4
move 2 from 1 to 3
move 1 from 1 to 2
move 2 from 4 to 1
"""