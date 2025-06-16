<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Support\Facades\Auth;

class StoreTemperatureEntryRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return Auth::check();
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'device_id' => ['required', 'exists:devices'],
            'temperature' => ['required', 'numeric', 'min:0', 'max:9000'],
            'humidity' => ['required', 'numeric', 'min:0', 'max:100'],
            'timestamp' => ['required', 'date'],
            'mock' => ['required', 'boolean']
        ];
    }
}
