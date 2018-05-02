def all_funcs( base, arity ):
    max = base**(base**arity)
    return { i for i in range( max ) }

def gen_out_cube( func_num, base, arity ):
    out = output_table( func_num, base, arity )
    return fold_cube( out, base, arity )

def output_table( num, base, arity ):
    size = base**arity
    output = get_digits( num, base, base**arity )
        
    return output

def get_digits( num, base, size ):
    output = []
    for i in range( size ):
        output.append( num % base )
        num //= base
    return output
        
def hypercube( dim ):
    return fold_cube( [i for i in range( dim**dim )], dim, dim )
    
def fold_cube( vals, side, dim ):
    if dim < 2:
        return vals
    
    for _ in range( 1, dim ):
        vals = [ vals[i:i+side] for i in range( 0, len(vals), side ) ]
        
    return vals
    
def unfold_cube( cube, dim ):
    if dim < 2:
        return cube
        
    for _ in range( 1, dim ):
        cube = [ i for j in cube for i in j ]
        
    return cube

def rotate_cube( cube, dim ):
    if dim <= 1:
        return cube

    cube = [ list(i) for i in zip(*cube) ]
    if dim > 2:
        for i in range( len(cube) ):
            cube[i] = rotate_cube( cube[i], dim-1 )
    return cube

def gen_offset( side, dim ):
    for i in range( side**dim ):
        off = get_digits( i, side, dim )
        if 0 in off:
            yield off
        
def pos_diagonals( cube, side, dim ):
    dia = []
    for off in gen_offset( side, dim ):
        diagonal = []
        for i in range( max( off ), side ):
            temp = cube
            for j in off:
                temp = temp[i-j]
            diagonal.append( temp )
        dia.append( diagonal )
    
    return dia

def is_monotonic( table, side, dim ):
        
    # Recursively Check Lower Dimensions
    for i in range( dim ):
        if not monotonic_recursive( table, side, dim ):
            return False
        table = rotate_cube( table, dim )
        
    return True

def monotonic_recursive( table, side, dim ):
    
    #Base Cases
    if dim < 1:
        return True
    if dim == 1:
        return is_mono_list( table )
        
    for i in range( side ):
        if not monotonic_recursive( table[i], side, dim-1 ):
            return False
            
    return True
        
'''
def is_monotonic( table, side, dim, parent_rec=0 ):

    # Base Cases
    if dim < 1:
        return True        
    if dim == 1:
        return is_mono_list( table )

    # Check Topmost Dimension's Diagonals
    for i in [ d for d in pos_diagonals( table, side, dim ) if len(d) > 1 ]:
        if not is_mono_list( i ):
            return False
    
    # Recursively Check Lower Dimensions        
    for i in range( parent_rec, dim ):
        for j in range(side):
            if not is_monotonic( table[j], side, dim-1, i ):
                return False
        table = rotate_cube( table, dim )
        
    return True
'''
        
def is_mono_list( lst ):
    #is_mono_list.num += 1
    for i in range( 1, len(lst) ):
        if lst[i-1] > lst[i]:
            return False
    return True
#is_mono_list.num = 0
 
'''def is_monotonic( table, base, arity ):
    out = output_table( func_num, base, arity )
    out = fold_cube( out, base, arity )
    return is_mono_rec( out, base, arity, 0 )
'''
    
def is_const_list( lst ):

    if len(lst) < 1:
        return True

    return all( i == lst[0] for i in lst[1:] )
    
def is_changing_list( lst ):
    s = set()
    return not any( i in s or s.add(i) for i in lst )
    
def is_affine( table, base, arity ):
    #out = output_table( func_num, base, arity )
    #out = fold_cube( out, base, arity )

    temp = table

    for _ in range(arity):
        rows = unfold_cube( temp, arity-1 )
        if is_const_list( rows[0] ):
            for row in rows[1:]:
                if not is_const_list( row ):
                    return False
        elif is_changing_list( rows[0] ):
            for row in rows[1:]:
                if not is_changing_list( row ):
                    return False
        else:
            return False
        temp = rotate_cube( temp, arity )
    return True

def is_self_dual( table, base, arity ):
    #out = output_table( func_num, base, arity )

    dual = [ base-1-i for i in table ]
    dual = dual[::-1]
    
    return table == dual
    
def is_value_preserving( table, base, arity, value ):
    #out = output_table( func_num, base, arity )
    
    index = value * (base**(arity)-1)//(base-1)
    return table[index] == value
    
def gen_compliments( base, arity ):
    all = all_funcs( base, arity )
    
    mono = set()
    affine = set()
    dual = set()
    val_keep = [set()]*base
    for func_num in all:
        flat_out = output_table( func_num, base, arity )
        out_cube = fold_cube( flat_out, base, arity )
        
        if is_monotonic( out_cube, base, arity ):
            mono.add( func_num )
        if is_affine( out_cube, base, arity ):
            affine.add( func_num )
        if is_self_dual( flat_out, base, arity ):
            dual.add( func_num )
            
        for i in range( base ):
            if is_value_preserving( flat_out, base, arity, i ):
                val_keep[i].add( func_num )
                
    rtrn = { 'NM':all-mono, 'NA':all-affine, 'ND':all-dual }
    for i in range( base ):
        rtrn['N'+str(i)] = all-val_keep[i]
        
    return rtrn
        











