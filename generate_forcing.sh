while [[ $# > 1 ]]
do
key="$1"

case $key in
    -r|--region)
    REGION="$2"
    shift # past argument
    ;;
    -d|--dates)
    DATES="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done


if [ -z "$REGION" ] && [ -z "$DATES"]; then
  echo ""
  echo "error: domain boundaries and timeframe have to be specified!"
  echo ""
  echo "usage: $0 -r N/W/S/E -d YYYY-MM-DD/to/YYYY-MM-DD"
  echo "  N/W/S/E ... northern/western/southern/eastern longitude/latitude of domain"
  echo ""
  exit
fi

echo "specified region: $REGION"
echo "specified dates : $DATES"

echo "called retrieve_erainterim.py - this might take a while..."
python ~/bin/erai2icar/retrieve_erainterim.py $REGION $DATES > generate_forcing.log
echo "...[done]"

echo "called forcing_assembly.py..."
python ~/bin/erai2icar/forcing_assembly.py erai_atm.nc erai_sfc.nc icar_forcing.nc >> generate_forcing.log
echo "...[done]" 

