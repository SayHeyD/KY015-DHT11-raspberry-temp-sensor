<?php

namespace App\Http\Controllers;

use App\Models\Device;
use Illuminate\Http\Request;
use Laravel\Jetstream\Jetstream;

class DeviceApiTokenController extends Controller
{
    public function store(Request $request)
    {
        $request->validate([
            'device_id' => ['required', 'exists:devices,id'],
            'name' => ['required', 'string', 'max:255'],
        ]);

        $device = Device::find($request->device_id);

        $token = $device->createToken(
            $request->name,
            Jetstream::validPermissions($request->input('permissions', []))
        );

        return back()->with('flash', [
            'token' => explode('|', $token->plainTextToken, 2)[1],
        ]);
    }

    /**
     * Update the given API token's permissions.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $tokenId
     * @return \Illuminate\Http\RedirectResponse
     */
    public function update(Request $request, $tokenId)
    {
        $request->validate([
            'device_id' => ['required', 'exists:devices,id'],
            'permissions' => 'array',
            'permissions.*' => 'string',
        ]);

        $device = Device::find($request->device_id);

        $token = $device->tokens()->where('id', $tokenId)->firstOrFail();

        $token->forceFill([
            'abilities' => Jetstream::validPermissions($request->input('permissions', [])),
        ])->save();

        return back(303);
    }

    /**
     * Delete the given API token.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $tokenId
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Request $request, $tokenId)
    {
        $request->validate([
            'device_id' => ['required', 'exists:devices,id'],
        ]);

        $device = Device::find($request->device_id);

        $device->tokens()->where('id', $tokenId)->first()->delete();

        return back(303);
    }
}
