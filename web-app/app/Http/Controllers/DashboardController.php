<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DashboardController extends Controller
{
    public function view(Request $request)
    {
        $devices = Auth::user()->devices;
        $selectedDeviceId = $request->query('device', $devices->first()->id);
        $currentDevice = $devices->find($selectedDeviceId);

        $devices->find($selectedDeviceId);

        $temperatures = $currentDevice->temperatures()
            ->where('created_at', '>=', now()->subDay())
            ->orderBy('created_at', 'desc')
            ->get();

        return Inertia::render('Dashboard/View', [
            'devices' => $devices,
            'temperatures' => $temperatures,
            'selectedDeviceId' => $selectedDeviceId
        ]);
    }
}
