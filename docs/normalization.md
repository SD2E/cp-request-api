# request normalization

normal form is sum of products

rep(c, b) = prod(b,..., b), arity c
gen(t, a, v1,..,vk) = sum(t[a/v1],..., t[a/vk]) 

prod(prod(b1,..,bk), prod(c1,...,cj)) = prod(b1,...,bk,c1,...,cj)

prod(b, sum(c1,...,ck)) = sum(prod(b, c1),...,prod(b,ck))
prod(sum(b1,...,bk),c) = sum(prod(b1, c),..., prod(bk, c))

prod(b1,...,bk) = prod(b1, prod(b2,...,bk))
prod(sum(b1,...,bk), sum(c1,...,cn)) = sum(prod(bi,cj) | i=1..k, j=1..n)

treatment = attribute | entity 
subject = entity