<?php

use App\Http\Controllers\TemperatureEntryController;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')
    ->prefix('/v1')
    ->name('api.v1.')
    ->group(function () {
        Route::prefix('/temperatures')->name('temperatures.')->group(function () {
            Route::post('/store', [TemperatureEntryController::class, 'store'])->name('store');
        });
});
