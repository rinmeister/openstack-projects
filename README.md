# Een python script om in openstack projecten aan te maken. Je moet als admin
kunnen aanmelden. Het script verwacht variabelen daarvoor in de environment
of in de ~/.config/openstack/clouds.yaml.

Voorbeeld van een environment setup:
export OS_AUTH_URL=http://1.2.3.4:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_PASSWORD=<password>
export OS_PROJECT_DOMAIN_NAME=<The name of domain containing the project>
export OS_PROJECT_NAME=<project name>
export OS_TENANT_NAME=<project name>
export OS_USERNAME=<username>
export OS_USER_DOMAIN_NAME=<The user's domain name>

Het script leest een yaml file waar een lijst in kan van usernames waar
projecten voor aangemaakt worden. De naam van het project is de username
Ook worden er rechten gezet op het project. De gebruiker wordt met de rol
'member' geconfigureerd. Daarnaast is er de mogelijkheid om een lijst van
usernames op te geven die voor elk aangemaakt project als admin worden ge-
configureerd.

Dit script wordt gebruikt op een beroepsopleiding om lab projecten klaar
te zetten voor studenten. De studenten krijgen ieder een eigen project met
hun eigen gebruikersnaam als projectnaam. Er is een lijst met docenten die
van elk project admin moeten worden gemaakt om te kunnen troubleshooten.
