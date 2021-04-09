#!/bin/bash

function current_datetime {
python3 -<<END
import datetime
print datetime.datetime.now()
END
julia - <<END
using JWAS
END
}
