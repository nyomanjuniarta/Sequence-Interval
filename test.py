import sys
from DAGPattern import Pattern, PatternConfig, pattern_parser, spmf2tuple
from diagram import init_diagram, add_intent, add_object, clean_flags

if __name__ == "__main__":
    theta = 1
    cfg = PatternConfig(theta)

    p1 = Pattern(config=cfg, dirty=False)
    p1.sequences = [[[1, 2, 5, 6], [2, 9, 5, 8]]]
    print 'p1.sequences', p1.sequences

    p2 = Pattern(config=cfg, dirty=False)
    p2.sequences = [[[1, 1, 5, 5]]]
    print 'p2.sequences', p2.sequences

    #print p1.intersect(p2).sequences

    p3 = Pattern(config=cfg, dirty=False)
    p3.sequences = [[[3, 4, 5, 8]], [[1, 2, 5, 6], [5, 9, 4, 8]]]
    print 'p3.sequences', p3.sequences

    p4 = Pattern(config=cfg, dirty=False)
    p4.sequences = [[[8, 9, 1, 6], [1, 2, 5, 6], [5, 9, 4, 8]], [[3, 4, 5, 8]]]
    print 'p4.sequences', p4.sequences

    p5 = Pattern(config=cfg, dirty=False)
    p5.sequences = [[[3, 4, 5, 8]], [[8, 9, 1, 6], [1, 2, 5, 6], [5, 9, 4, 8]]]
    print 'p5.sequences', p5.sequences

    p6 = Pattern(config=cfg, dirty=False)
    p6.sequences = [[[50.5, 51.0, 45.6, 46.1], [3.1, 4.0, 8.3787, 9.1]]]
    print 'p6.sequences', p6.sequences

    p7 = Pattern(config=cfg, dirty=False)
    p7.sequences = [[[50.5, 50.8, 45.6, 46.1], [3.1, 3.8, 8.3787, 9.06]], [[1.0, 2.0, 1.0, 2.0]]]
    print 'p7.sequences', p7.sequences

    '''print 'p1 <= p4', p1 <= p4
    print 'p3 <= p4', p3 <= p4
    print 'p3 <= p1', p3 <= p1
    print 'p2 <= p4', p2 <= p4
    print 'p5 == p4', p5 == p4
    print 'p6 <= p7', p6 <= p7'''

    p8 = Pattern(config=cfg, dirty=False)
    p8.sequences = [[[3, 3, 5, 6]], [[8, 9, 1, 2], [1, 2, 5, 6], [5, 6, 6.8, 8]]]
    print 'p8.sequences', p8.sequences

    p9 = Pattern(config=cfg, dirty=False)
    p9.sequences = [[[3, 4, 5, 6]], [[8, 9, 1, 2], [1, 2, 5, 6], [10, 11, 9, 10], [5, 6, 7, 8]]]
    print 'p9.sequences', p9.sequences

    print 'p8 n p9', p8.intersect(p9).sequences
