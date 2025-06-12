<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreDeviceRequest;
use App\Http\Requests\UpdateDeviceRequest;
use App\Models\Device;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DeviceController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        return Inertia::render('Device/Index', [
            'devices' => $user->devices,
        ]);
    }

    public function show(Device $device)
    {
        return Inertia::render('Device/Show', [
            'device' => $device,
        ]);
    }

    public function create()
    {
        return Inertia::render('Device/Create');
    }

    public function store(StoreDeviceRequest $request)
    {
        $user = Auth::user();
        $device = $user->devices()->create($request->validated());

        return redirect()->route('devices.show', $device->id)
            ->banner("Created device '$device->name'");
    }

    public function update(Device $device, UpdateDeviceRequest $request)
    {
        $device->update($request->validated());
        return redirect()->route('devices.show', $device)
            ->banner("Updated device '$device->name'");
    }

    public function destroy(Device $device)
    {
        $device->delete();
        return redirect()->route('devices.index')
            ->banner("Deleted device '$device->name'");
    }
}
