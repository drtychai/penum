#!/bin/bash
shopt -s extglob

oct2bin=("000" "001" "010" "011" "100" "101" "110" "111")

function squishtogether {
        result=""
        while (($#)) ; do
                result="${result}${1}"
                shift
        done
        echo $result
}

function splitapart {
        string=$1
        result=""
        while ((${#string})) ; do
                rest=${string#?}
                chr=${string%$rest}
                if [[ -z $result ]] ; then
                        result=$chr
                else
                        result="${result} ${chr}"
                fi
                string=$rest
        done
        echo $result
}

function addzeros {
# will also remove zeros if needed
        ZS=$2
        NUM=$1
        NUM=${NUM##+(0)}
        NUM=$(printf "%0${ZS}d\n" $NUM)
        echo $NUM
}

function bin2dec {
        string="2#${1}"
        ((idec=$string))
        echo $idec
}

function dec2bin {
        result=""
        for i in $(splitapart $(printf "%3o" $1)) ; do
                result="${result}${oct2bin[i]}"
        done
        echo $result
}

function ipbin2ip {
   cont=1
   for l in $(splitapart $1); do
      VIPTMP[$cont]=$l
      ((cont=cont+1))
   done
   ONE=`bin2dec $(squishtogether ${VIPTMP[@]:1:8})`
   TWO=`bin2dec $(squishtogether ${VIPTMP[@]:9:8})`
   THREE=`bin2dec $(squishtogether ${VIPTMP[@]:17:8})`
   FOUR=`bin2dec $(squishtogether ${VIPTMP[@]:25:8})`
   echo ${ONE}.${TWO}.${THREE}.${FOUR}
}
IPCIDR=$1
IP=${IPCIDR%/*}
BITS=${IPCIDR#*/}

FST=${IP%%.*}
IP=${IP#*.}
FSTBIN=`addzeros $(dec2bin "$FST") 8`
SND=${IP%%.*}
IP=${IP#*.}
SNDBIN=`addzeros $(dec2bin "$SND") 8`
TRD=${IP%%.*}
FOH=${IP#*.}
TRDBIN=`addzeros $(dec2bin "$TRD") 8`
FOHBIN=`addzeros $(dec2bin "$FOH") 8`

VIP=0.0.0.0
IPBIN="$FSTBIN$SNDBIN$TRDBIN$FOHBIN"

i=1
for l in $(splitapart $IPBIN); do
   VIPBIN[$i]="$l"
   ((i=i+1))
done

BITSHOST=$(expr 32 - $BITS)
i=$BITSHOST
while (( $i > 0 )); do
   MAXHOSTBIN=1$MAXHOSTBIN
   ((i=i-1))
done
MAXHOST=$(bin2dec $MAXHOSTBIN)

n=$(squishtogether ${VIPBIN[@]:1:$BITS})
c=$MAXHOST
while (( $c > 0 )); do
   h=$c
   EUREKA=${n}$(addzeros `dec2bin $h` $BITSHOST)
   ipbin2ip "$EUREKA"
   c=$(expr $c - 1)
done
