# sonarr-sqlite-csv-to-postgres
This repository contains a script that makes migrating from sonarr using sqlite to postgres a little easier.

I'm not very good at explaining things so let me try to do my best.

This script is if pgloader doesn't work for you like in the guide mentioned below on wiki.servarr.com

Backup your sonarr database by going here: IP_OF_SONARR_INSTANCE:PORT/system/backup and click Backup Now.
Click the latest backup to download it to your computer.
You're going to need the sonarr.db file later.
So follow this guide like normal: https://wiki.servarr.com/sonarr/postgres-setup.
When you get to the migrating data step, come here and follow the rest of this guide.
Download this program that allows you to dump an sqlite database/tables to csv files: https://sqlitebrowser.org/dl/
Open up sonarr.db in sqlite browser. Go to File -> Export -> Table(s) as csv files.
Select all tables except for sqlite_sequence. 
Make sure Column Names in First Line is checked and click OK.
Once it finishes dumping all of the tables to csv.

Okay here is where it is trial and error until it completes without issue. You may have to modify your files a little to get it to not complain:
Go into your database via pgadmin or some other tool and run this query:

<code>DELETE from "AutoTagging";
DELETE from "Blocklist";
DELETE from "Commands";
DELETE from "Config";
DELETE from "CustomFilters";
DELETE from "CustomFormats";
DELETE from "DelayProfiles";
DELETE from "DownloadClientStatus";
DELETE from "DownloadClients";
DELETE from "DownloadHistory";
DELETE from "EpisodeFiles";
DELETE from "Episodes";
DELETE from "ExtraFiles";
DELETE from "History";
DELETE from "ImportListExclusions";
DELETE from "ImportListItems";
DELETE from "ImportListStatus";
DELETE from "ImportLists";
DELETE from "IndexerStatus";
DELETE from "Indexers";
DELETE from "Metadata";
DELETE from "MetadataFiles";
DELETE from "NamingConfig";
DELETE from "NotificationStatus";
DELETE from "Notifications";
DELETE from "PendingReleases";
DELETE from "QualityDefinitions";
DELETE from "QualityProfiles";
DELETE from "ReleaseProfiles";
DELETE from "RemotePathMappings";
DELETE from "RootFolders";
DELETE from "SceneMappings";
DELETE from "ScheduledTasks";
DELETE from "Series";
DELETE from "SubtitleFiles";
DELETE from "Tags";
DELETE from "Users";
DELETE from "VersionInfo";</code>

Make sure the username, password, and host is configured on this line:
<code>engine = create_engine('postgresql://username:password@127.0.0.1:5432/sonarr-main')</code>
Run the python module using idle or terminal if it doesn't make it to the end, then run all of the delete statements again, fix the error in one of the csv files and try running the python module once more.
I have this working with postgres 17. 
If you have an issue, please create an issue and I will try to fix the problem. I'm slow to fix things in my hobby projects so please be aware of this.
