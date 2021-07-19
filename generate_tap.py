def generate_tap_v2(dsn, grids, tlib, templates, iter_type='nppn', iter_type_end=None, transform_type='0X0X', transform_type_end=None, side='both'): 
    """ This function generates taps on the left, right or both side of the design.
        parameters:
            iter_type:          list of transistor types for iteration. Even if there should be ptap, the type is 'n' since there are NMOS on the design.
            iter_type_end:      list of transistor types after the iteration
            transform_type:     list of transform types of each iterating tap cell
            transform_type_end: list of transform types of each tap cell after iteration
            side:               tap generation side. both / left / right

        iter_type and transform_type should have identical length.
    """

    pg         = grids["placement_basic"]           # Load basic placement grid for placing taps.
    height_tap = grids["routing_23_cmos"].height//2 # Calculate the height of tap which is generally the half of the CMOS height.
    
    bbox             = dsn.bbox                         # The bbox of the design.
    height_dsn       = bbox[1][1]                       # The height of the design.
    total_num_of_tap = np.int(bbox[1][1] // height_tap) # Total number of taps. 8 taps are needed if there are 4 CMOS grids in the design. 5 taps if 2 CMOS grids and 1 half-CMOS.
    iter_len         = len(iter_type)                   # length of iteration

    print('total number of taps: ' + str(total_num_of_tap))

    ltap_list = []
    rtap_list = [] 
    if total_num_of_tap%iter_len == 0: # full iteration
        for idx in range(total_num_of_tap//iter_len): # number of iteration
            i=0
            for celltype in iter_type: # in each iteration
                ltap = templates[celltype+'mos4_fast_tap'].generate(name='LTAP'+str(idx)+str(i), transform='R0' if transform_type[i]=='0' else 'MX')
                rtap = templates[celltype+'mos4_fast_tap'].generate(name='RTAP'+str(idx)+str(i), transform='R0' if transform_type[i]=='0' else 'MX')
                ltap_list.append(ltap)
                rtap_list.append(rtap)
                i+=1
        if side == 'both':
            dsn.place(grid=pg, inst=np.array(rtap_list).reshape(len(rtap_list),1), mn=pg.mn.bottom_right(bbox))
            dsn.place(grid=pg, inst=np.array(ltap_list).reshape(len(ltap_list),1), mn=pg.mn.bottom_left(bbox) - pg.mn.width_vec(ltap))
        elif side == 'left':
            dsn.place(grid=pg, inst=np.array(ltap_list).reshape(len(ltap_list),1), mn=pg.mn.bottom_left(bbox) - pg.mn.width_vec(ltap))
        elif side == 'right':
            dsn.place(grid=pg, inst=np.array(rtap_list).reshape(len(rtap_list),1), mn=pg.mn.bottom_right(bbox))

    else: # iteration + extra taps
        for idx in range((total_num_of_tap-len(iter_type_end))//iter_len):
            i=0
            for celltype in iter_type:
                ltap = templates[celltype+'mos4_fast_tap'].generate(name='LTAP'+str(idx)+str(i), transform='R0' if transform_type[i]=='0' else 'MX')
                rtap = templates[celltype+'mos4_fast_tap'].generate(name='RTAP'+str(idx)+str(i), transform='R0' if transform_type[i]=='0' else 'MX')
                ltap_list.append(ltap)
                rtap_list.append(rtap)
                i+=1

        for idx in range(len(iter_type_end)):
            i=0
            for celltype in iter_type_end:
                ltap = templates[celltype+'mos4_fast_tap'].generate(name='LTAPEND'+str(idx)+str(i), transform='R0' if transform_type_end[i]=='0' else 'MX')
                rtap = templates[celltype+'mos4_fast_tap'].generate(name='RTAPEND'+str(idx)+str(i), transform='R0' if transform_type_end[i]=='0' else 'MX')
                ltap_list.append(ltap)
                rtap_list.append(rtap)
                i+=1
        if side == 'both':
            dsn.place(grid=pg, inst=np.array(rtap_list).reshape(len(rtap_list),1), mn=pg.mn.bottom_right(bbox))
            dsn.place(grid=pg, inst=np.array(ltap_list).reshape(len(ltap_list),1), mn=pg.mn.bottom_left(bbox) - pg.mn.width_vec(ltap))
        elif side == 'left':
            dsn.place(grid=pg, inst=np.array(ltap_list).reshape(len(ltap_list),1), mn=pg.mn.bottom_left(bbox) - pg.mn.width_vec(ltap))
        elif side == 'right':
            dsn.place(grid=pg, inst=np.array(rtap_list).reshape(len(rtap_list),1), mn=pg.mn.bottom_right(bbox))
