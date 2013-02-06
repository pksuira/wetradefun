
def sort(unsorted_list, sort_field, asc_or_desc):
    """ Sorts a list in place using insetion sort.
    
    unsorted_list - a list to be sorted
    sort_field - attribute of each element to sort the entire list by
        (each element must have this attribute)
    asc_or_desc - result wanted in ascending or descending order?
        must be either "asc" or "desc"

    """    

    h = unsorted_list
    index = 0
    comparing = index + 1

    # insertion sort ascending
    while (comparing < len(h)):
        if (getattr(h[index], sort_field) > getattr(h[comparing], sort_field)):
            h.insert(index, h[comparing])
            index = index + 1
            comparing = comparing - 1
            del(h[index+1])

            while (comparing > 0):
                if (getattr(h[comparing], sort_field) < getattr(h[comparing-1], sort_field)):
                    h.insert(comparing-1, h[comparing])
                    del(h[comparing+1])
                    comparing = comparing - 1
                else:
                    break

            comparing = index + 1
        else:
            index = index + 1
            comparing = index + 1

    # if want desc, reverse list
    if (asc_or_desc == "asc"):
        return h
    elif (asc_or_desc == "desc"):
        return h.reverse()
    else:
        raise NotImplementedError, "'" + asc_or_desc + "' must either be 'asc' or 'desc'"
