<?php

use App\Http\Controllers\DashboardController;
use App\Http\Controllers\IndexController;
use Illuminate\Support\Facades\Route;

Route::get('/', [IndexController::class, 'view'])->name('index');

Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified',
])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'view'])->name('dashboard');
});
