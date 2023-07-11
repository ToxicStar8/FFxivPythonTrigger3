const zoom_property_default = {zoom: {min: 0, max: 0}, fov: {min: 0, max: 0}, angle: {min: 0, max: 0}}
module.exports = vue.defineComponent({
    name: 'XivCombo',
    props: ['plugin'],
    setup(props) {
        const {plugin} = vue.toRefs(props);
        return {plugin, zoom_property_default}
    },
    template: `
<el-form label-position="left" label-width="200px">
    <h4>Combat</h4>
    <fpt-bind-item attr="speed_percent" :plugin="plugin" v-slot="{value}">
        <el-form-item label="移速">
             <el-slider v-model="value.value" :step="0.05" :min="0" :max="2" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="jump" :plugin="plugin" v-slot="{value}">
        <el-form-item label="跳跃高度">
             <el-slider v-model="value.value" :step="0.1" :min="0" :max="20" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="swing_reduce" :plugin="plugin" v-slot="{value}">
        <el-form-item label="减少咏唱时间">
             <el-slider v-model="value.value" :step="0.01" :min="0" :max="10" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="skill_animation_lock_time" :plugin="plugin" v-slot="{value}">
        <el-form-item label="动画锁(必须开启本地动画锁)">
             <el-slider v-model="value.value" :step="0.01" :min="0" :max="1" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="skill_animation_lock_local" :plugin="plugin" v-slot="{value}">
        <el-form-item label="本地动画锁">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="hit_box_adjust" :plugin="plugin" v-slot="{value}">
        <el-form-item label="扩大目标圈">
             <el-slider v-model="value.value" :step="0.5" :min="0" :max="5" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="anti_knock" :plugin="plugin" v-slot="{value}">
        <el-form-item label="防击退">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="ninja_stiff" :plugin="plugin" v-slot="{value}">
        <el-form-item label="断绝无后摇">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="afix_enable" :plugin="plugin" v-slot="{value}">
        <el-form-item label="瞬移打身位">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="afix_distance" :plugin="plugin" v-slot="{value}">
        <el-form-item label="瞬移打身位有效距离">
             <el-slider v-model="value.value" :step="0.1" :min="0" :max="10" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="moving_swing_enable" :plugin="plugin" v-slot="{value}">
        <el-form-item label="移动施法">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="moving_swing_time" :plugin="plugin" v-slot="{value}">
        <el-form-item label="移动施法时间">
             <el-slider v-model="value.value" :step="0.1" :min="0" :max="5" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="moving_no_fall" :plugin="plugin" v-slot="{value}">
        <el-form-item label="无下落伤害(飞行会掉线)">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="moving_z_modify" :plugin="plugin" v-slot="{value}">
        <el-form-item label="飞天遁地距离">
             <el-slider v-model="value.value" :step="0.5" :min="-20" :max="20" show-input/>
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="no_misdirect" :plugin="plugin" v-slot="{value}">
        <el-form-item label="无视目押">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="no_forced_march" :plugin="plugin" v-slot="{value}">
        <el-form-item label="无视强制移动">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="no_hysteria" :plugin="plugin" v-slot="{value}">
        <el-form-item label="无视恐慌">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="action_no_move" :plugin="plugin" v-slot="{value}">
        <el-form-item label="突进不位移">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="action_no_move_some" :plugin="plugin" v-slot="{value}">
        <el-form-item label="action_no_move_some">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <el-divider/>
    <h4>Zoom</h4>
    <fpt-bind-item attr="zoom_cam_distance_reset"  :plugin="plugin" v-slot="{value}">
        <el-form-item label="视角距离不重置">
            <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="zoom_cam_no_collision" :plugin="plugin" v-slot="{value}">
        <el-form-item label="视角无视障碍">
            <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item :default_value="zoom_property_default" attr="zoom_property" :plugin="plugin" v-slot="{value}">
        <el-form-item label="视距">
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.zoom.min" />
            </el-col>
            <el-col class="line" :span="2">&nbsp;-&nbsp;</el-col>
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.zoom.max" />
            </el-col>
        </el-form-item>
        <el-form-item label="fov">
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.fov.min" />
            </el-col>
            <el-col class="line" :span="2">&nbsp;-&nbsp;</el-col>
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.fov.max" />
            </el-col>
        </el-form-item>
        <el-form-item label="角度">
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.angle.min" />
            </el-col>
            <el-col class="line" :span="2">&nbsp;-&nbsp;</el-col>
            <el-col :span="11">
                <el-input type="number" v-model.number="value.value.angle.max" />
            </el-col>
        </el-form-item>
    </fpt-bind-item>
    <el-button @click="plugin.run_single('apply_zoom')" class="w-100">apply zoom</el-button>
    <el-divider/>
    <fpt-bind-item attr="stalk_vis" :plugin="plugin" v-slot="{value}">
        <el-form-item label="跟踪任务不会被发现">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="cutscene_skip" :plugin="plugin" v-slot="{value}">
        <el-form-item label="主随跳动画">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="all_cutscenes_skip_enable_1" :plugin="plugin" v-slot="{value}">
        <el-form-item label="跳所有动画 1">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="all_cutscenes_skip_enable_2" :plugin="plugin" v-slot="{value}">
        <el-form-item label="跳所有动画 2">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="all_cutscenes_skip_enable_3" :plugin="plugin" v-slot="{value}">
        <el-form-item label="跳所有动画 3">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="no_kill_enable" :plugin="plugin" v-slot="{value}">
        <el-form-item label="掉线不会退游戏">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="no_kill_skip_auth" :plugin="plugin" v-slot="{value}">
        <el-form-item label="认证失败不会退游戏">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="anti_afk" :plugin="plugin" v-slot="{value}">
        <el-form-item label="挂机防踢">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <fpt-bind-item attr="enable_anti_chat_block" :plugin="plugin" v-slot="{value}">
        <el-form-item label="屏蔽词解限">
             <el-switch v-model="value.value" />
        </el-form-item>
    </fpt-bind-item>
    <el-divider/>
</el-form>
`
})
