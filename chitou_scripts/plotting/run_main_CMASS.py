python cmp_main_CMASS.py -1 CMASS -2 CMASS -m ser -n ser -b i -x mtot -y mtot --title "SExtractor(aperture) vs PyMorph(Sersic)" --bins "19.5,22.01,0.5" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "19.5,22.5" --xtM 1 --xtm 0.25  --ylab 'm$_{\mathrm{tot, SEx}}$-m$_{\mathrm{tot,PyM}}$' --xlab 'm$_{\mathrm{tot,PyM}}$'

python cmp_main_CMASS.py -1 CMASS -2 CMASS -m ser -n ser -b i -x mtot -y hrad --title "SExtractor(aperture) vs PyMorph(Sersic)" --bins "19.5,22.01,0.5" --yl "-1.0,1.0" --ytM 0.5 --ytm 0.05 --xl "19.5,22.5" --xtM 1 --xtm 0.25  --ylab '1 - (r$_{\mathrm{SEx}}$/r$_{\mathrm{PyM}}$)$_{\mathrm{hl}}$' --xlab 'm$_{\mathrm{tot,PyM}}$'