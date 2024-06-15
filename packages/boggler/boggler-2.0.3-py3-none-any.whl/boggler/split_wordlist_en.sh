#!/bin/sh

if [ -z $1 ] || [ -z $2 ]; then
    echo "Usage: WORDLIST OUT_DIR"
    exit 0
else
    rg "(^a[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_a.txt"
    rg "(^b[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_b.txt"
    rg "(^c[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_c.txt"
    rg "(^d[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_d.txt"
    rg "(^e[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_e.txt"
    rg "(^f[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_f.txt"
    rg "(^g[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_g.txt"
    rg "(^h[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_h.txt"
    rg "(^i[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_i.txt"
    rg "(^j[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_j.txt"
    rg "(^k[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_k.txt"
    rg "(^l[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_l.txt"
    rg "(^m[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_m.txt"
    rg "(^n[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_n.txt"
    rg "(^o[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_o.txt"
    rg "(^p[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_p.txt"
    rg "(^q[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_q.txt"
    rg "(^r[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_r.txt"
    rg "(^s[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_s.txt"
    rg "(^t[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_t.txt"
    rg "(^u[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_u.txt"
    rg "(^v[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_v.txt"
    rg "(^w[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_w.txt"
    rg "(^x[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_x.txt"
    rg "(^y[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_y.txt"
    rg "(^z[a-z]+).*$" -or '$1' $1 | sort | uniq > "$2/words_z.txt"
    touch "$2/words__.txt"
    exit 0
fi
