#!/usr/bin/bash

eval "$(conda shell.bash hook)"
conda activate /home/eliot.finch/eos/env/

### script that conditions agnostic processes on different compositions
### NOTE, this does not include EFT predictions
### Reed Essick (reed.essick@gmail.com)

#-------------------------------------------------
#
# define the source of our "tabluated EoS from the literature"
#
#-------------------------------------------------

declare -A hdf5paths
declare -A selectparampath

basedir="$PWD"

### add hadagn stuff

dir="${basedir}/hadagn"

hdf5paths['had']="${hdf5paths['had']} ${dir}/bsk/gpr_gpr_hadronic-bsk.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/bsr/gpr_gpr_hadronic-bsr.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/dd/gpr_gpr_hadronic-dd.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/eng/gpr_gpr_hadronic-eng.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/gm/gpr_gpr_hadronic-gm.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/kde/gpr_gpr_hadronic-kde.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/mpa/gpr_gpr_hadronic-mpa.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/nl/gpr_gpr_hadronic-nl.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/r/gpr_gpr_hadronic-r.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/sk/gpr_gpr_hadronic-sk.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/sly/gpr_gpr_hadronic-sly.hdf5"
hdf5paths['had']="${hdf5paths['had']} ${dir}/tm/gpr_gpr_hadronic-tm.hdf5"

selectparampath['had']="${dir}/hyperparams-mc_hadronic-agnostic.csv"

### add hypagn stuff

dir="${basedir}/hypagn"

hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/bsr/gpr_gpr_hyperonic-bsr.hdf5"
hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/dd/gpr_gpr_hyperonic-dd.hdf5"
hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/gm/gpr_gpr_hyperonic-gm.hdf5"
hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/h/gpr_gpr_hyperonic-h.hdf5"
hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/nl/gpr_gpr_hyperonic-nl.hdf5"
hdf5paths['hyp']="${hdf5paths['hyp']} ${dir}/tm/gpr_gpr_hyperonic-tm.hdf5"

selectparampath['hyp']="${dir}/hyperparams-mc_hyperonic-agnostic.csv"

### add qrkagn stuff

dir="${basedir}/qrkagn"

hdf5paths['qrk']="${hdf5paths['qrk']} ${dir}/alf/gpr_gpr_quark-alf.hdf5"
hdf5paths['qrk']="${hdf5paths['qrk']} ${dir}/ddq/gpr_gpr_quark-ddq.hdf5"
hdf5paths['qrk']="${hdf5paths['qrk']} ${dir}/hqc/gpr_gpr_quark-hqc.hdf5"

selectparampath['qrk']="${dir}/hyperparams-mc_quark-agnostic.csv"

#-------------------------------------------------
#
# define parameters used to construct conditioned processes
#
#-------------------------------------------------

# Resolution of the GP
num_points=500

# The number of hyperparameter sets to use (out of ~ 300)
num_models=50

# pQCD predictions give pH ~ 1e16
min_pressurec2="1e10"
max_pressurec2="1e16"
min_pressure=$(python -c "from universality import utils ; print(utils.c**2*${min_pressurec2})")
max_pressure=$(python -c "from universality import utils ; print(utils.c**2*${max_pressurec2})")

pressure_bounds="$min_pressure $max_pressure"

#------------------------

# To try and control the low density behaviour (now that we're not using the
# stitch there) we use a higher reference pressure (which controls where its 
# attached to the crust)
integrate_phi_reference_pressure="3e11"

# Old value (I guess?)
# integrate_phi_reference_pressure="3e10"

#------------------------

# We're now stitching at high pressures
min_stitch_pressurec2="1e14"
max_stitch_pressurec2="1e16"

# For cs^2/c^2 = 1/3, we require phi = log(3 - 1) = log(2) ~ 0.69
stitch_mean=0.6931471805599453 
stitch_pressurec2="1e16"
stitch_index=-3.0
stitch_sigma=0.1

stitch_num_points=100

#---

min_stitch_pressure=$(python -c "from universality import utils ; print(utils.c**2*${min_stitch_pressurec2})")
max_stitch_pressure=$(python -c "from universality import utils ; print(utils.c**2*${max_stitch_pressurec2})")
stitch_pressure=$(python -c "from universality import utils ; print(utils.c**2*${stitch_pressurec2})")

stitch_pressure_bounds="$min_stitch_pressure $max_stitch_pressure"

#------------------------

temperature="inf"

CRUST="$PWD/ingo-bps-with-cs2c2-modified.csv"

#-------------------------------------------------
#
# actually construct the conditioned processes
#
#-------------------------------------------------

# Number of EoS realizations we want
NUM_EOS=100000

#------------------------

COMPS=""
COMPS="$COMPS qrk"

#------------------------

for COMP in $COMPS
do

    tag="${COMP}agn"
    outdir="${PWD}/${tag}"

    echo "--------------------------------------------------"
    echo "PROCESSING $tag"

    #-------------------------------------

    hdf5model=${outdir}/gpr_gpr_${tag}.hdf5

    #-------------------------------------

    ### integrate the samples
    samples="" # used to record options for plotting later

    for i in $(seq 0 $(($NUM_EOS-1)))
    do

        I=$(python -c "print('%06d'%$i)")
        M=$(python -c "print('%06d'%($i//1000))")
        phipath="${outdir}/DRAWmod1000-$M/draw-gpr_${tag}-${I}.csv"
        outpath="${outdir}/DRAWmod1000-$M/eos-draw-${I}.csv"

        samples="$samples -s $I $outpath --samples-alpha $I 0.25 --samples-color $I k"

        # echo \
        integrate-phi \
            -v \
            -o $outpath \
            --sigma-logpressurec2 0.0 \
            --stitch-below-reference-pressure \
            --crust $CRUST \
            --include-cs2c2 \
            $phipath $integrate_phi_reference_pressure \
        || exit 1

        echo $i >> $process ### add this EoS realization to manifest

    done

    #-------------------------------------

done

