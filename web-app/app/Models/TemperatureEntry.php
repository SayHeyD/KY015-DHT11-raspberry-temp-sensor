<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class TemperatureEntry extends Model
{
    /** @use HasFactory<\Database\Factories\TemperatureEntryFactory> */
    use HasFactory;

    protected $keyType = 'string';
    public $incrementing = false;

    protected $fillable = [
        'device_id',
        'temperature',
        'humidity',
    ];

    public function device(): BelongsTo
    {
        return $this->belongsTo(Device::class);
    }
}
