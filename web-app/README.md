# rtsa web-app

Simple web-app to view sensor log data. This is a Laravel application. Example deploy script:

```shell
cd web-app/
git pull origin main
composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev
# PHP-FPM reload has automatically been moved to the post deploy script.

npm i
npm run build

php artisan route:cache
php artisan view:clear
php artisan migrate --force
```

