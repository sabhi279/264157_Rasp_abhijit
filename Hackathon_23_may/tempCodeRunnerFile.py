    def show_image(self, img_cv):
        self.canvas.delete("all")  # Clear canvas

        if len(img_cv.shape) == 2:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
        else:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        h, w = img_cv.shape[:2]
        scale = min(600/w, 400/h)
        img_resized = cv2.resize(img_cv, (int(w*scale), int(h*scale)))

        img_pil = Image.fromarray(img_resized)
        self.tk_img = ImageTk.PhotoImage(img_pil)

        self.canvas.config(width=img_resized.shape[1], height=img_resized.shape[0])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
